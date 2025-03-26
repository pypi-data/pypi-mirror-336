# Proteomics Converter
A Python package to convert between `somadata.Adat` and input required by `pandora`.

## Installation
Requires Python>=3.9.
### Installation with pip:
```shell
pip install proteomics-converter --extra-index-url https://ussd.artifactory.illumina.com/api/pypi/pypi-bioinfo/simple 
```
### Installation with poetry:
```shell
# Add ilmn pypi as source
poetry source add --priority=supplemental ilmn https://ussd.artifactory.illumina.com/api/pypi/pypi-bioinfo/simple
# Install package from ilmn pypi
poetry add proteomics-converter --source ilmn
```

## Usage

### Converting an adat object to pandora inputs
`adat_to_pandora_input` converts an adat object to `PandoraInput`:
- counts dataframe in long format, with three columns `count_col`, `somamer_index_col`, `sample_index_col`
- sample metadata dataframe
- somamer metadata dataframe
- adat header as dictionary
```python
from proteomics_converter.adat_func import adat_to_pandora_input

pandora_input = adat_to_pandora_input(
   adat=adat,
   count_col='Count_Raw',
   somamer_index_col='SeqId',
   sample_index_col='SampleID',
)
```

### Converting pandora inputs to an adat object
`pandora_input_to_adat` is the reverse of `adat_to_pandora_input` that converts pandora input to an adat object.
```python
from proteomics_converter.adat_func import pandora_input_to_adat, PandoraInput

adat = pandora_input_to_adat(
    pandora_input=PandoraInput(counts=counts, sample_metadata=sample_metadata, somamer_metadata=somamer_metadata, header_metadata=header_metadata),
    sample_index_col='SampleID',
    somamer_index_col='SeqId',
    count_col='Count',
)
```



