from process_csv import CSVinfo, find_process_csv
from builtin_descriptions import builtin_descriptions
import logging
from bids.layout import BIDSLayout
import logging
import os.path as op
import json


# inputs
bids_layout_path = "/Users/john/AFQ_data/HCP_1200"
bids_layout_kwargs = {}
list_of_CSVinfo = [CSVinfo(
    {"space": "RASMM", "suffix": "count"},
    "afq",
    ["n_streamlines", "n_streamlines_clean"]
)]
html_bids_filters = {"suffix": "viz"}
html_in_derivative = "afq"
custom_descriptions = {}


logger = logging.getLogger('NIRV.Parser')

merged_dfs = None
for csv_info in list_of_CSVinfo:
    deriv_folder = op.join(
        bids_layout_path,
        "derivatives",
        csv_info.derivative_folder)
    bids_layout = BIDSLayout(
        bids_layout_path, derivatives=deriv_folder, **bids_layout_kwargs)

    df, has_sess = find_process_csv(csv_info, bids_layout)
    if merged_dfs is None:
        merged_dfs = df
    elif has_sess:
        merged_dfs.merge(df, on=['participantID', 'sessionID'], how='outer')
    else:
        merged_dfs.merge(df, on='participantID', how='outer')

if html_in_derivative is None:
    html_in_derivative = False
else:
    html_in_derivative = op.join(
        bids_layout_path,
        "derivatives",
        html_in_derivative)
bids_layout_html = BIDSLayout(
    bids_layout_path, derivatives=html_in_derivative, **bids_layout_kwargs)

for index, row in merged_dfs.iterrows():
    participant_filters = {"subject": row["participantID"]}
    if "sessionID" in row:
        participant_filters["session"] = row["sessionID"]

    all_filters = {**html_bids_filters, **participant_filters}
    all_filters["extension"] = "html"
    found_html = bids_layout_html.get(**all_filters)
    if len(found_html) < 1:
        logger.warning(f"No HTML found with filters: {all_filters}")
    else:
        if len(found_html) > 1:
            logger.warning((
                f"More than one HTML found with filters: {all_filters}. "
                f"The following path was chosen: {found_html[0].path}"))
        merged_dfs.loc[index, "path_to_html_report"] = found_html[0].path
merged_dfs.to_csv(
    op.join(
        bids_layout_path,
        f"nirv_group_report.csv"),
    index=False)

to_json = {"variables": []}
this_descriptions = builtin_descriptions.copy()
this_descriptions.update(custom_descriptions)
for column_name in merged_dfs.columns:
    if column_name in ["participantID", "sessionID", "path_to_html_report"]:
        continue
    to_json["variables"].append({
        "name": column_name,
        "description": this_descriptions.get(
            column_name, f"Please provide a descrition for: {column_name}"),
        "type": str(df.dtypes[column_name])})

with open(op.join(bids_layout_path, "nirv_group_report.json"), "w") as ff:
    json.dump(to_json, ff)
