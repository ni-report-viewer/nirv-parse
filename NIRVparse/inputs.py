from dataclasses import dataclass, field
from typing import Union
from NIRVparse.process_csv import CSVinfo


__all__ = ["Inputs", "get_pyafq_inputs"]


@dataclass
class Inputs:
    bids_layout_path: str
    list_of_CSVinfo: list
    bids_layout_kwargs: dict = field(default_factory=lambda: {})
    html_bids_filters: dict = field(default_factory=lambda: {})
    html_in_derivative: Union[str, None] = None
    custom_descriptions: dict = field(default_factory=lambda: {})


def get_pyafq_inputs(bids_layout_path):
    return Inputs(
        bids_layout_path,
        [CSVinfo(
            {"space": "RASMM", "suffix": "count"},
            "afq",
            ["n_streamlines", "n_streamlines_clean"])],
        {},
        {"suffix": "viz"},
        "afq",
        {}
    )


def get_qsiprep_inputs(bids_layout_path, in_deriv):
    bids_layout_kwargs = {"validate": False}
    csv_filters = {"suffix": "dwi"}
    csv_occlusion = [
        "file_name", "subject_id", "session_id", "task_id", "dir_id",
        "acq_id", "space_id", "rec_id", "run_id"]
    if in_deriv:
        return Inputs(
            bids_layout_path,
            [CSVinfo(
                csv_filters,
                "qsiprep",
                [],
                csv_occlusion)],
            bids_layout_kwargs,
            {},
            "qsiprep")
    else:
        return Inputs(
            bids_layout_path,
            [CSVinfo(
                csv_filters,
                None,
                [],
                csv_occlusion)],
            bids_layout_kwargs
        )
