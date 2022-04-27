from dataclasses import dataclass, field
import logging
import os.path as op
import dask.dataframe as dd


__all__ = ["CSVinfo", "find_process_csv"]


logger = logging.getLogger('NIRV.ProcessCSV')


@dataclass
class CSVinfo:
    """
    Information for finding a CSV per subject (optionally per session)
    using BIDS filters in a given derivatives folder.

    Parameters
    ----------
    bids_filters : dict
        Filter to pass to bids_layout.get when finding CSV files.
    derivative_folder : str
        Name of derivatives folder which contains the CSV.
    value_names_to_wide : list, optional
        List of value names to use to pivot the CSV from long to wide.
        Use this if each row does not already correspond to a participantID
        or sessionID. If the list is empty, perform no pivot.
        Default: []
    """
    bids_filters: dict
    derivative_folder: str
    value_names_to_wide: list = field(default_factory=lambda: [])


def find_process_csv(csv_info, bids_layout):
    v_names = csv_info.value_names_to_wide
    csv_info.bids_filters["extension"] = "csv"
    found_csvs = bids_layout.get(**csv_info.bids_filters)
    logger.info(
        f"# of files found with filter {csv_info.bids_filters}: {len(found_csvs)}")
    df = dd.read_csv(found_csvs, include_path_column=True).compute()

    # pivot if necessary
    if len(v_names) > 0:
        c_names = list(df.columns)
        for v_name in v_names:
            c_names.remove(v_name)
        c_names.remove("path")
        df = df.pivot(index="path", columns=c_names, values=v_names)
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
    else:
        df.index = df["path"]
        df = df.drop(columns="path")

    # add participantID, sessionID (optional) columns
    cols_to_move = ['participantID']
    df["participantID"] = df.index.map(
        lambda x: x.split("sub-")[1].split("/")[0])
    if "ses-" in df.index[0]:
        df["sessionID"] = df.index.map(
            lambda x: x.split("ses-")[1].split("/")[0])
        cols_to_move.append("sessionID")
        has_sess = True
    else:
        has_sess = False
    df = df.reset_index(drop=True)
    df = df[cols_to_move + [col for col in df.columns if col not in cols_to_move]]

    return df, has_sess
