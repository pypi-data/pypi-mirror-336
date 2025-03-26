from pathlib import Path
from typing import Union

import yaml

# dict to convert adat entries to instrument_info format
# this might change if pandora is upgraded
META_FROM_ADAT = ('!NGSLot', '!RunId', '!InstrumentType', '!Flowcell')
META_FROM_INSTRUMENT_INFO = ('ngs_lot', 'run_id', 'instrument', 'flow_cell')
ADAT_TO_INSTRUMENT_INFO_DICT = dict(zip(META_FROM_ADAT, META_FROM_INSTRUMENT_INFO))
INSTRUMENT_INFO_TO_ADAT_DICT = dict(zip(META_FROM_INSTRUMENT_INFO, META_FROM_ADAT))


def create_yml_from_dict(
        header_dict: dict,
        yaml_file: Union[str, Path],
        replace_keys_dict: dict = None,
) -> None:
    """convert adat header to yaml file, it will act as instrument_into_file with all the required entries"""
    # rename keys in header_dict according to INSTRUMENT_DICT
    if replace_keys_dict is None:
        replace_keys_dict = INSTRUMENT_INFO_TO_ADAT_DICT
    header_dict = {replace_keys_dict.get(k, k): v for k, v in header_dict.items()}
    with open(yaml_file, 'w') as f:
        yaml.dump(header_dict, f)


def insert_instrument_info_into_adat_header(
        adat_header: dict,
        instrument_info_yml: Union[str, Path],
        replace_keys_dict: dict = None,
) -> dict:
    """insert instrument info into adat header dict"""
    if replace_keys_dict is None:
        replace_keys_dict = ADAT_TO_INSTRUMENT_INFO_DICT
    with open(instrument_info_yml) as f:
        instrument_info = yaml.safe_load(f)
    # rename keys in instrument_info according to replace_keys_dict
    instrument_info = {replace_keys_dict.get(k, k): v for k, v in instrument_info.items()}
    # add instrument info to adat header
    return {**adat_header, **instrument_info}

