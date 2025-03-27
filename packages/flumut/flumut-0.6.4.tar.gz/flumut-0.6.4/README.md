<p align="center">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="docs/images/flumut_logo_w.png">
      <source media="(prefers-color-scheme: light)" srcset="docs/images/flumut_logo_b.png">
      <img alt="FluMut logo." src="docs/images/flumut_logo_b.png">
    </picture>
</p>

[![GitHub Release](https://img.shields.io/github/v/release/izsvenezie-virology/FluMut?label=FluMut)](https://github.com/izsvenezie-virology/FluMut/releases/latest/)
[![GitHub Release](https://img.shields.io/github/v/release/izsvenezie-virology/FluMutDB?label=FluMutDB)](https://github.com/izsvenezie-virology/FluMutDB/releases/latest/)
[![GitHub Release](https://img.shields.io/github/v/release/izsvenezie-virology/FluMutGUI?label=FluMutGUI)](https://github.com/izsvenezie-virology/FluMutGUI/releases/latest/)

[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/flumut/README.html)
[![install with pip](https://img.shields.io/badge/install%20with-pip-brightgreen.svg)](https://pypi.org/project/flumut/)

FluMut is an open-source tool designed to search for molecular markers with potential impact on the biological characteristics of Influenza A viruses of the A(H5N1) subtype, starting from complete or partial nucleotide genome sequences.

For the complete documentation please visit [FluMut site](https://izsvenezie-virology.github.io/FluMut/).

## Installation

### Prerequisites

FluMut is available for Windows, Linux and macOS.

### Pip

FluMut is available on [PyPI](https://pypi.org/project/flumut/).
Before installing FluMut via Pip you need:

- [Python](https://www.python.org/downloads/)
- [Pip](https://pypi.org/project/pip/) (often packaged with Python)

Then, you can install FluMut with this command:

```
pip install flumut
```

### Bioconda

FluMut is also available on [Bioconda](https://bioconda.github.io/flumut).
You can install using Conda or Mamba.

- [Mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) (recommended)

```
mamba install -c bioconda flumut
```

- [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

```
conda install -c bioconda flumut
```

### FluMutGUI

The graphical version at the moment is available only for Windows OS.
We plan to release it also for MacOS and Linux.
[Download](https://github.com/izsvenezie-virology/FluMutGUI/releases/latest/download/FluMutGUI_Installer.exe) the installer and follow the instructions.
Check out how to use it on [complete documentation](https://izsvenezie-virology.github.io/FluMut/docs/usage/usage-gui).

## Usage

## Input

FluMut can analyze multiple A(H5N1) Influenza virus sequences simultaneously.
It can handle partial and complete genome sequences of multiple samples.
You must provide a single file containing all the nucleotide sequences in FASTA format.
Sequences must adhere to the [IUPAC code](https://www.bioinformatics.org/sms/iupac.html).

FluMut relies on the FASTA header to assign the sequence to a specific segment and sample.
For this reason, the header must contain both a sample ID (consistent among sequences of the same sample) and one of the following segment names: `PB2`, `PB1`, `PA`, `HA`, `NP`, `NA`, `MP`, `NS`.

An example of input file can be downloaded [here](https://github.com/izsvenezie-virology/FluMut/releases/latest/download/fasta_input_example.fa).

### Basic usage

You can get the output file in an [Excel format](#excel) (user-friendly) running:

```
flumut -x excel_output.xlsm your_fasta.fa
```

If you prefer the [text outputs](#text-outputs) (machine-readable format) run:

```
flumut -m markers_output.tsv -M mutations_output.tsv -l literature_output.tsv your_fasta.fa
```

### Update database

You should always use the latest version of our database and you can do it just by running this command:

```
flumut --update
```

## Outputs

FluMut can produce an Excel output or text outputs:

- [Excel](#excel)
- [Text outputs](#text-outputs)

By default FluMut reports only markers where all mutations are found.
You can report all markers where at least one mutation is found using option `-r`/`--relaxed`.

### Excel

This is the most user-friendly and complete output.
You can obtain this output using the `-x`/`--excel-output` option.
Find out more [here](https://izsvenezie-virology.github.io/FluMut/docs/output#excel-output).

> **_IMPORTANT:_** To enable the navigation feature the exstension of the Excel file must be `.xlsm`.
> If you don't care about navigation, you can use `.xlsx` exstension.
> Other exstensions lead to unreadable files.

### Text outputs

You can obtain 3 different text outputs:
| Option | Output | Desctription |
| -- | -- | -- |
| `-m`/`--markers-output` | [Markers output](https://izsvenezie-virology.github.io/FluMut/docs/output#markers-output) | List of detected markers |
| `-M`/`--mutations-output` | [Mutations output](https://izsvenezie-virology.github.io/FluMut/docs/output#mutations-output) | List of amino acids present in the positions of mutations of interest for each sample |
| `-l`/`--literature-output` | [Literature output](https://izsvenezie-virology.github.io/FluMut/docs/output#literature-output) | List of all papers present in the database |

## Cite FluMut

If you use FluMut, please cite:

> Giussani, E., Sartori, A. et al. (2025). FluMut: a tool for mutation surveillance in highly pathogenic H5N1 genomes. Virus Evolution, [10.1093/ve/veaf011](https://doi.org/10.1093/ve/veaf011).

## License

FluMut is licensed under the GNU Affero v3 license (see [LICENSE](LICENSE)).

# Fundings

This work was partially supported by the FLU-SWITCH Era-Net ICRAD (grant agreement No. 862605), by EU funding under the NextGeneration EU-MUR PNRR Extended Partnership initiative on Emerging Infectious Diseases (Project No. PE00000007, INF-ACT), and by KAPPA-FLU HORIZON-CL6-2022-FARM2FORK-02-03 (grant agreement No. 101084171).

<p align="center" margin="10px">
    <img style="height:80px;margin:8px" alt="Logo supporter, FLU-SWITCH" src="docs/images/Logo-Flu-Switch.png"/>
    <img style="height:80px;margin:8px" alt="Logo supporter, INF-ACT" src="docs/images/Logo-Inf-act.jpg"/>
    <img style="height:80px;margin:8px" alt="Logo supporter, European Union" src="docs/images/Logo-eu.png"/>
    <img style="height:80px;margin:8px" alt="Logo supporter, KAPPA-FLU" src="docs/images/logo-kappa-flu.jpg"/>
</p>

> Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Health and Digital Executive Agency (HEDEA).
> Neither the European Union nor the granting authority can be held responsible for them
