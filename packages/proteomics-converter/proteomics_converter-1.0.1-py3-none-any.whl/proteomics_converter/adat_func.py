import dataclasses
import re

import pandas as pd
import numpy as np
import somadata

from somadata import Adat


def infer_count_col_from_file_name(adat_name: str) -> str:
    """Infer count_col name to be used in long format CSV
    It can be removed once we have the normalization_step stored in adat
    """
    match = re.findall(
        r'(Count\_[a-zA-Z]+\.adat$)',
        adat_name,
    )
    if len(match) == 0:
        raise ValueError(f'{adat_name} does not contain Count_xxx.adat suffix. Unable to determine count column.')
    return match[0].rstrip('.adat')


def to_long(adat: Adat, count_col: str, sample_names: pd.Index = None, somamer_indexl_col: str = 'SeqId', sample_name: str = 'SampleID') -> pd.DataFrame:
    somamer_names = adat.columns.get_level_values(somamer_indexl_col)
    if sample_names is None:
        sample_names = adat.index.get_level_values(sample_name)
    data_wide = pd.DataFrame(adat.values, index=sample_names, columns=somamer_names).reset_index()
    return pd.melt(data_wide, id_vars=[sample_name], value_name=count_col)


@dataclasses.dataclass
class PandoraInput:
    counts: pd.DataFrame
    sample_metadata: pd.DataFrame
    somamer_metadata: pd.DataFrame
    header_metadata: dict


def adat_to_pandora_input(adat: somadata.Adat, **kwargs) -> PandoraInput:
    sample_metadata, somamer_metadata = adat.index.to_frame(index=False), adat.columns.to_frame(index=False)
    counts = to_long(adat, **kwargs)
    header_metadata = adat.header_metadata
    return PandoraInput(counts, sample_metadata, somamer_metadata, header_metadata)


def reorder_elements(elements_in_order: list, df: pd.DataFrame, map_col: str = None) -> pd.DataFrame:
    element_order_dict = dict(
        zip(
            elements_in_order,
            range(len(elements_in_order)),
        )
    )
    if map_col is None:
        element_index = np.argsort(df.index.map(element_order_dict))
    else:
        element_index = np.argsort(df[map_col].map(element_order_dict))
    return df.iloc[element_index]


def create_dfs_from_multiple_adat(adat_list: list[Adat]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sample_df, somamer_df, count_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    i = 0
    for adat in adat_list:
        sample_names = pd.Index([_ for _ in range(i, i + len(adat))], name='SampleID')
        i += len(adat)
        current_sample_df = adat.index.to_frame()
        current_sample_df['SampleIndex'] = sample_names.tolist()
        sample_df = pd.concat([sample_df, current_sample_df])
        somamer_df = pd.concat([somamer_df, adat.columns.to_frame()]).drop_duplicates('SeqId')
        count_df = pd.concat([count_df, to_long(adat=adat, count_col='Count', sample_names=sample_names)])

    count_df_wide = count_df.pivot(columns='SeqId', values='Count', index='SampleID').fillna(0)
    samples_in_order, somamers_in_order = count_df_wide.index.tolist(), count_df_wide.columns.tolist()
    reordered_somamer_df = reorder_elements(somamers_in_order, somamer_df, 'SeqId')
    reordered_sample_df = reorder_elements(samples_in_order, sample_df, 'SampleIndex')

    return reordered_sample_df, reordered_somamer_df, count_df_wide


def update_adat(
        original_adat: Adat,
        sample_index_col: str,
        seqid_index_col: str,
        count_wide: pd.DataFrame = None,
        sample_df: pd.DataFrame = None,
        seqid_df: pd.DataFrame = None,
):
    """Update count, sample_df, somamer_df of a given adat"""

    if count_wide is None:
        count_wide = pd.DataFrame(
            data=original_adat.values,
            index=original_adat.index.get_level_values(sample_index_col),
            columns=original_adat.columns.get_level_values(seqid_index_col),
        )
    if sample_df is None:
        sample_df = original_adat.index.to_frame()

    sample_df = reorder_elements(
        elements_in_order=count_wide.index.tolist(),
        df=sample_df,
        map_col=sample_index_col,
    )
    if seqid_df is None:
        seqid_df = original_adat.columns.to_frame()
    seqid_df = reorder_elements(
        elements_in_order=count_wide.columns.tolist(),
        df=seqid_df,
        map_col=seqid_index_col,
    )
    sample_metadata_dict = sample_df.to_dict(orient='list')
    somamer_metadata_dict = seqid_df.to_dict(orient='list')
    norm_adat = Adat.from_features(
        rfu_matrix=np.asmatrix(count_wide),
        row_metadata=sample_metadata_dict,
        column_metadata=somamer_metadata_dict,
        header_metadata={},
    )
    return norm_adat


def pandora_input_to_adat(
        count_col: str,
        sample_index_col: str,
        somamer_index_col: str,
        pandora_input: PandoraInput,
) -> somadata.Adat:
    """construct adat from pandora input.
    The constructed adat has the same sample and somamer order as pandora_input.sample_metadata and pandora_input.somamer_metadata respectively"""

    counts, sample_metadata, somamer_metadata, header_metadata = pandora_input.counts, pandora_input.sample_metadata, pandora_input.somamer_metadata, pandora_input.header_metadata
    counts_wide = pd.pivot_table(counts, values=count_col, index=sample_index_col, columns=somamer_index_col)
    counts_wide = reorder_elements(
        elements_in_order=sample_metadata[sample_index_col].tolist(),
        df=counts_wide,
    )
    counts_wide = reorder_elements(
        elements_in_order=somamer_metadata[somamer_index_col].tolist(),
        df=counts_wide,
    )
    return Adat.from_features(
        rfu_matrix=np.asmatrix(counts_wide),
        row_metadata=sample_metadata.to_dict(orient='list'),
        column_metadata=somamer_metadata.to_dict(orient='list'),
        header_metadata=header_metadata,
    )
