from NIRVparse.process_csv import find_process_csv
from NIRVparse.builtin_descriptions import builtin_descriptions
import logging
from bids.layout import BIDSLayout
import logging
import os.path as op
import json


logger = logging.getLogger('NIRV.Parser')

def gen_json(inputs):
    # merge input CSVs
    merged_dfs = None
    for csv_info in inputs.list_of_CSVinfo:
        deriv_folder = op.join(
            inputs.bids_layout_path,
            "derivatives",
            csv_info.derivative_folder)
        bids_layout = BIDSLayout(
            inputs.bids_layout_path, derivatives=deriv_folder,
            **inputs.bids_layout_kwargs)

        df, has_sess = find_process_csv(csv_info, bids_layout)
        if merged_dfs is None:
            merged_dfs = df
        elif has_sess:
            merged_dfs.merge(df, on=['participantID', 'sessionID'], how='outer')
        else:
            merged_dfs.merge(df, on='participantID', how='outer')

    # find HTML files
    if inputs.html_in_derivative is None:
        html_in_derivative = False
    else:
        html_in_derivative = op.join(
            inputs.bids_layout_path,
            "derivatives",
            inputs.html_in_derivative)
    bids_layout_html = BIDSLayout(
        inputs.bids_layout_path, derivatives=html_in_derivative,
        **inputs.bids_layout_kwargs)

    # generate NIRV group report CSV
    for index, row in merged_dfs.iterrows():
        participant_filters = {"subject": row["participantID"]}
        if "sessionID" in row:
            participant_filters["session"] = row["sessionID"]

        all_filters = {**inputs.html_bids_filters, **participant_filters}
        all_filters["extension"] = "html"
        found_html = bids_layout_html.get(**all_filters)
        if len(found_html) < 1:
            logger.warning(f"No HTML found with filters: {all_filters}")
        else:
            if len(found_html) > 1:
                logger.warning((
                    f"More than one HTML found with filters: {all_filters}. "
                    f"The following path was chosen: {found_html[0].path}"))
            merged_dfs.loc[index, "path_to_html_report"] = op.relpath(
                found_html[0].path, inputs.bids_layout_path)
    merged_dfs.to_csv(
        op.join(
            inputs.bids_layout_path,
            f"nirv_group_report.csv"),
        index=False)

    # generate NIRV group report JSON
    to_json = {"variables": []}
    this_descriptions = builtin_descriptions.copy()
    this_descriptions.update(inputs.custom_descriptions)
    for column_name in merged_dfs.columns:
        if column_name in ["participantID", "sessionID", "path_to_html_report"]:
            continue
        to_json["variables"].append({
            "name": column_name,
            "description": this_descriptions.get(
                column_name, f"Please provide a descrition for: {column_name}"),
            "type": str(df.dtypes[column_name])})

    with open(op.join(
            inputs.bids_layout_path, "nirv_group_report.json"), "w") as ff:
        json.dump(to_json, ff)
