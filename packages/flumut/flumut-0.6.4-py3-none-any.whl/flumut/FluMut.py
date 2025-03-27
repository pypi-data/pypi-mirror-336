import re
import sys
import operator
import itertools

from io import TextIOWrapper
from typing import Dict, Generator, List, Optional, Tuple

from collections import defaultdict
from Bio.Align import PairwiseAligner

from flumut.DbReader import close_connection, execute_query, open_connection, to_dict
from flumut import OutputFormatter
from flumut.DataClass import Mutation, Sample
from flumut.Exceptions import UnmatchNameException, UnknownSegmentException, UnknownNucleotideException, MalformedFastaException

PRINT_ALIGNMENT = False


def start_analysis(name_regex: str, fasta_file: TextIOWrapper,
                   markers_output: TextIOWrapper, mutations_output: TextIOWrapper, literature_output: TextIOWrapper, excel_output: str,
                   relaxed: bool, skip_unmatch_names: bool, skip_unknown_segments: bool, verbose: bool) -> None:
    '''
    Find markers of zoonotic interest in H5N1 avian influenza viruses.
    '''

    if verbose:
        print('LOG: Initializing FluMut...', file=sys.stderr)
    # Initialization
    samples: Dict[str, Sample] = {}
    pattern = re.compile(name_regex)

    if verbose:
        print('LOG: Loading data from FluMutDB...', file=sys.stderr)

    open_connection()
    segments = load_segments()
    mutations = load_mutations()
    annotations = load_annotations()
    close_connection()

    # Per sequence analysis
    for name, seq in read_fasta(fasta_file):
        if verbose:
            print(f'LOG: Processing {name}', file=sys.stderr)

        sample,  segment = parse_name(name, pattern, skip_unmatch_names)
        if sample is None or segment is None:
            continue
        if segment not in segments:
            ex = UnknownSegmentException(name, pattern.pattern, segment)
            if not skip_unknown_segments:
                raise ex
            print(ex.message, file=sys.stderr)
            continue

        if sample not in samples:
            samples[sample] = Sample(sample)

        reference_name, reference_sequence = select_reference(segments[segment], seq)
        ref_align, sample_align = pairwise_alignment(reference_sequence, seq)

        for protein, cds in annotations[reference_name].items():
            ref_cds, sample_cds = get_cds(ref_align, sample_align, cds)
            ref_aa = ''.join(translate(ref_cds))
            sample_aa = translate(sample_cds)

            samples[sample].mutations += find_mutations(
                ref_aa, sample_aa, sample, mutations[protein])

    if verbose:
        print(f'LOG: Collecting markers...', file=sys.stderr)

    open_connection()
    for sample in samples.values():
        sample.markers = match_markers(sample.mutations, relaxed)
    papers = load_papers()
    close_connection()

    if verbose:
        print('LOG: Preparing outputs...', file=sys.stderr)
    found_mutations = list(itertools.chain.from_iterable(mutations.values()))
    found_mutations.sort(key=operator.attrgetter('protein', 'pos', 'alt'))

    # Outputs
    if mutations_output:
        if verbose:
            print(f'LOG: Writing "{mutations_output.name}"...', file=sys.stderr)
        header, data = OutputFormatter.mutations_dict(found_mutations)
        OutputFormatter.write_csv(mutations_output, header, data)

    if markers_output:
        if verbose:
            print(f'LOG: Writing "{markers_output.name}"...', file=sys.stderr)
        header, data = OutputFormatter.markers_dict(samples.values())
        OutputFormatter.write_csv(markers_output, header, data)

    if literature_output:
        if verbose:
            print(f'LOG: Writing "{literature_output.name}"...', file=sys.stderr)
        header, data = OutputFormatter.papers_dict(papers)
        OutputFormatter.write_csv(literature_output, header, data)

    if excel_output:
        if verbose:
            print(f'LOG: Writing "{excel_output}"...', file=sys.stderr)
        wb = OutputFormatter.get_workbook(excel_output.endswith('.xlsm'))
        header, data = OutputFormatter.mutations_dict(found_mutations)
        wb = OutputFormatter.write_excel_sheet(wb, 'Mutations', header, data)
        header, data = OutputFormatter.markers_dict(samples.values())
        wb = OutputFormatter.write_excel_sheet(wb, 'Markers', header, data)
        header, data = OutputFormatter.papers_dict(papers)
        wb = OutputFormatter.write_excel_sheet(wb, 'Literature', header, data)
        wb = OutputFormatter.save_workbook(wb, excel_output)

    if verbose:
        print(f'LOG: Analysis complete.', file=sys.stderr)


def load_mutations() -> Dict[str, List[Mutation]]:
    mutations = defaultdict(list)
    res = execute_query(""" SELECT reference_name, protein_name, name, type, ref_seq, alt_seq, position
                            FROM mutation_mappings
                            JOIN mutations ON mutation_mappings.mutation_name = mutations.name""")
    for mut in res:
        mutations[mut[1]].append(Mutation(*mut[2:]))
    return mutations


def load_segments() -> Dict[str, Dict[str, str]]:
    res = execute_query("SELECT segment_name, name, sequence FROM 'references'")
    segments = defaultdict(dict)
    for segment, name, sequence in res:
        segments[segment][name] = sequence
    return segments


def load_annotations() -> Dict[str, Dict[str, List[Tuple[int, int]]]]:
    res = execute_query("SELECT reference_name, protein_name, start, end FROM 'annotations'")
    ann = defaultdict(lambda: defaultdict(list))
    for ref, prot, start, end in res:
        ann[ref][prot].append((start, end))
    return ann


def load_papers() -> List[Dict[str, str]]:
    return execute_query("""SELECT  id AS 'Short name',
                                    title AS 'Title',
                                    authors AS 'Authors',
                                    year AS 'Year',
                                    journal AS 'Journal',
                                    web_address AS 'Link',
                                    doi AS 'DOI'
                            FROM papers""", to_dict).fetchall()


def match_markers(muts: List[Mutation], relaxed: bool) -> List[Dict[str, str]]:
    muts_str = ','.join([f"'{mut.name}'" for mut in muts])
    res = execute_query(f"""
    WITH markers_tbl AS (SELECT marker_id,
                                group_concat(mutation_name) AS found_mutations,
                                count(mutation_name) AS found_mutations_count
                            FROM markers_mutations
                            WHERE mutation_name IN ({muts_str})
                            GROUP BY markers_mutations.marker_id)

    SELECT  markers_summary.all_mutations AS 'Marker',
            markers_tbl.found_mutations AS 'Mutations in your sample',
            markers_effects.effect_name AS 'Effect', 
            group_concat(markers_effects.paper_id, '; ') AS 'Literature', 
            markers_effects.subtype AS 'Subtype'
    FROM markers_effects
    JOIN markers_tbl ON markers_tbl.marker_id = markers_effects.marker_id
    JOIN markers_summary ON markers_summary.marker_id = markers_effects.marker_id
    WHERE markers_effects.marker_id IN (
        SELECT markers_tbl.marker_id 
        FROM markers_tbl) {'AND markers_summary.all_mutations_count = markers_tbl.found_mutations_count' if not relaxed else ''}
    GROUP BY markers_effects.marker_id, markers_effects.effect_name, markers_effects.subtype
    """, to_dict)
    return res.fetchall()


def select_reference(references: Dict[str, str], ref_seq: str) -> Tuple[str, str]:
    if len(references) > 1:
        NotImplementedError('Selection for reference from segments with more than one is not yet implemented')
    (name, sequence), = references.items()
    return name, sequence


def find_mutations(ref_aa: str, sample_aa: List[str], sample_name: str, mutations: List[Mutation]):
    found_mutations = []
    for mutation in mutations:
        pos = adjust_position(ref_aa, mutation.pos)
        mutation.samples[sample_name] = sample_aa[pos]
        if mutation.alt in sample_aa[pos]:
            mutation.found = True
            found_mutations.append(mutation)
    return found_mutations


def pairwise_alignment(ref_seq: str, sample_seq: str) -> Tuple[str, str]:
    '''Align sequence against a reference'''
    aligner = PairwiseAligner()
    aligner.mismatch_score = -1
    aligner.open_gap_score = -5
    aligner.extend_gap_score = -1
    aligner.query_left_open_gap_score = 1
    aligner.query_right_open_gap_score = 1
    aligner.target_left_open_gap_score = 1
    aligner.target_right_open_gap_score = 1
    alignment = aligner.align(ref_seq, sample_seq)[0]
    if PRINT_ALIGNMENT:
        print(alignment, file=sys.stderr)
    return alignment[0], alignment[1]


def read_fasta(fasta_file: TextIOWrapper) -> Generator[str, None, None]:
    '''Create a Fasta reading a file in Fasta format'''
    name = None
    for raw_line in fasta_file:
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith('>'):
            if name is not None:
                yield name, ''.join(seq).replace('-', '').upper()
            name = line[1:]
            seq = []
        else:
            try:
                seq.append(line)
            except UnboundLocalError:
                raise MalformedFastaException() from None
    if name is not None:
        yield name, ''.join(seq).upper()


def parse_name(name: str, pattern: re.Pattern, force: bool) -> Tuple[str, str]:
    '''Get sample and segment information by sequence name'''
    match = pattern.match(name)
    try:
        sample = match.groupdict().get('sample', match.group(1))
        seg = match.groupdict().get('segment', match.group(2))
    except (IndexError, AttributeError):
        ex = UnmatchNameException(name, pattern.pattern)
        if not force:
            raise ex from None
        print(ex.message, file=sys.stderr)
        return None, None
    else:
        return sample, seg


def translate(seq: str) -> List[str]:
    '''Translate nucleotidic sequence in AA sequence'''
    nucls = list(seq)
    aas = []
    is_first = True

    for i in range(0, len(nucls), 3):
        codon = get_codon(nucls, i, is_first)
        aa = translate_codon(codon)
        if aa not in ('-', '?'):
            is_first = False
        aas.append(aa)
    return aas


def get_codon(seq: List[str], start: int, is_first: bool) -> List[str]:
    '''Exctract the codon'''
    codon = seq[start:start + 3]
    if codon == ['-', '-', '-']:  # If the codon is a deletion
        return codon
    # If the codon starts from mid codon (to avoid frameshifts in truncated sequences):
    if is_first and '-' in codon:
        return codon
    if 'N' in codon:
        return codon
    codon = [n for n in codon if n != '-']
    while len(codon) < 3:
        next_nucl = find_next_nucl(seq, start)
        if not next_nucl:
            break
        codon.append(seq[next_nucl])
        seq[next_nucl] = '-'
    return codon


def translate_codon(codon: List[str]) -> str:
    '''Translate a codon into a set of AAs, containing all possible combinations in case of degenerations'''
    if 'N' in codon:
        return '?'
    try:
        undegenerated_codon = [degeneration_dict[nucl] for nucl in codon]
    except KeyError:
        raise UnknownNucleotideException(''.join(codon)) from None
    codons = list(itertools.product(*undegenerated_codon))
    aas = [translation_dict.get(''.join(c), '?') for c in codons]
    return ''.join(sorted(set(aas)))


def find_next_nucl(seq: List[str], start: int) -> Optional[int]:
    '''Returns the position of the next non deleted nucleotide'''
    for i in range(start + 3, len(seq)):
        if not seq[i] == '-':
            return i
    return None


def get_cds(ref_seq: str, sample_seq: str, cds: List[Tuple[int, int]]) -> Tuple[str, str]:
    '''Cut and assemble the nucleotide sequences based on positions given by the cds'''
    cds.sort(key=lambda x: x[0])
    ref_nucl = ''
    sample_nucl = ''

    for rng in cds:
        start = adjust_position(ref_seq, rng[0])
        end = adjust_position(ref_seq, rng[1]) + 1
        ref_nucl += ref_seq[start:end]
        sample_nucl += sample_seq[start:end]
    return ref_nucl, sample_nucl


def adjust_position(ref_seq: str, pos: int) -> int:
    '''Adjust 1-based position to 0-based, considering reference sequence gaps'''
    pos -= 1    # conversion 1-based to 0-based numeration
    dashes = 0
    adj_pos = pos
    while ref_seq.count('-', 0, adj_pos + 1) != dashes:
        dashes = ref_seq.count('-', 0, adj_pos + 1)
        adj_pos = pos + dashes
    return adj_pos


translation_dict = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M', 'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*', 'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K', 'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W', 'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
    '---': '-'
}


degeneration_dict = {
    'A': ['A'], 'C': ['C'], 'G': ['G'], 'T': ['T'], 'U': ['T'], '-': ['-'],
    'R': ['A', 'G'], 'Y': ['C', 'T'], 'S': ['G', 'C'], 'W': ['A', 'T'],
    'K': ['G', 'T'], 'M': ['A', 'C'], 'B': ['C', 'G', 'T'], 'D': ['A', 'G', 'T'],
    'H': ['A', 'C', 'T'], 'V': ['A', 'C', 'G'], 'N': ['A', 'C', 'G', 'T']
}
