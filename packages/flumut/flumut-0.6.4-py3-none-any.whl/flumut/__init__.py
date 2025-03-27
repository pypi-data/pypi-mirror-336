__version__ = '0.6.4'
__author__ = 'Edoardo Giussani'
__contact__ = 'egiussani@izsvenezie.it'

import sys
from typing import Dict
from io import TextIOWrapper

from flumut import Updater
from flumut.FluMut import start_analysis
from flumut.DbReader import get_db_version, set_db_file


def versions() -> Dict[str, str]:
    """Collect versions of FluMut and FluMutDB packages.

    Returns:
    versions : `Dict[str, str]`
            Versions for FluMut and FluMutDB packages.
    """

    major, minor, date = get_db_version()
    return {
        'FluMut': __version__,
        'FluMutDB': f'{major}.{minor}, released on {date}'
    }


def update() -> None:
    """Updates FluMutDB package using Pip.
    """
    Updater.update()


def update_db_file() -> None:
    """Updates FluMutDB database without updating FluMutDB
    """
    Updater.update_db_file()


def analyze(name_regex: str, fasta_file: TextIOWrapper, db_file: str,
            markers_output: TextIOWrapper, mutations_output: TextIOWrapper, literature_output: TextIOWrapper, excel_output: str,
            relaxed: bool = False, skip_unmatch_names: bool = False, skip_unknown_segments: bool = False,
            debug: bool = False, verbose: bool = False) -> None:
    """Runs the FluMut analysis.

    Args:
        name_regex: `str`
            The regex used to parse FASTA header
        fasta_file: `TextIOWrapper`
            The opened FASTA file to analyze
        db_file: `str|None`
            Path of the db file. If `None` the file from FluMutDB is used
        markers_output: `TextIOWrapper|None`
            The opened file where write Markers output
        mutations_output: `TextIOWrapper|None`
            The opened file where write Mutations output
        literature_output: `TextIOWrapper|None`
            The opened file where write Literature output
        excel_output: `str`
            The complete path to the Excel output file
        relaxed: `bool`
            When `True`, all markers where at least one mutation is detected
        skip_unmatch_names: `bool`
            When `True`, unmatching names do not raise exceptions
        skip_unknown_segments: `bool`
            When `True`, unknown segments do not raise exceptions
    """

    if not debug:
        sys.tracebacklimit = 0

    if name_regex is None:
        name_regex = r'(?P<sample>.+)_(?P<segment>.+)'
    if db_file is not None:
        set_db_file(db_file)

    start_analysis(name_regex=name_regex,
                   fasta_file=fasta_file,
                   markers_output=markers_output,
                   mutations_output=mutations_output,
                   literature_output=literature_output,
                   excel_output=excel_output,
                   relaxed=relaxed,
                   skip_unmatch_names=skip_unmatch_names,
                   skip_unknown_segments=skip_unknown_segments,
                   verbose=verbose)
