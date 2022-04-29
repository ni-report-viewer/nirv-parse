__all__ = ["builtin_descriptions"]

pyafq_bundles = [
    'CCMid',
    'ML_R',
    'Temporal',
    'VOF_R',
    'CNIV_L',
    'ARC_L',
    'DLF_L',
    'STT_R',
    'AR_L',
    'SLF_L',
    'SLF_R',
    'RST_R',
    'ILF_L',
    'ILF_R',
    'DLF_R',
    'CT_R',
    'ARC_R',
    'MLF_L',
    'CC_ForcepsMajor',
    'OR_L',
    'SCP',
    'CNVII_L',
    'MCP',
    'CNII_L',
    'CST_L',
    'AST_L',
    'CNVIII_R',
    'CB_L',
    'RST_L',
    'C_R',
    'MdLF_R',
    'UF_L',
    'IFO_L',
    'IFOF_L',
    'FPT_R',
    'CC_ForcepsMinor',
    'IFOF_R',
    'Orbital',
    'TPT_L',
    'OPT_R',
    'CB_R',
    'VOF_L',
    'Occipital',
    'CNV_L',
    'STT_L',
    'CTT_R',
    'CS_L',
    'EMC_R',
    'SupFrontal',
    'CNVII_R',
    'UNC_R',
    'Motor',
    'LL_R',
    'CC',
    'CNIV_R',
    'PC',
    'ATR_L',
    'AF_L',
    'CTT_L',
    'CNVIII_L',
    'TPT_R',
    'AF_R',
    'AR_R',
    'AntFrontal',
    'ICP_R',
    'PPT_R',
    'PostParietal',
    'FA',
    'CNIII_L',
    'OR_R',
    'CNV_R',
    'AST_R',
    'UF_R',
    'CNII_R',
    'CT_L',
    'FPT_L',
    'V',
    'ML_L',
    'C_L',
    'CGC_L',
    'EMC_L',
    'CS_R',
    'CGC_R',
    'PPT_L',
    'LL_L',
    'F_L_R',
    'IFO_R',
    'MLF_R',
    'ATR_R',
    'FP',
    'SupParietal',
    'ICP_L',
    'OPT_L',
    'CST_R',
    'CNIII_R',
    'UNC_L',
    'MdLF_L',
    'AC',
    'whole_brain']


builtin_descriptions = {}
for bundle_name in pyafq_bundles:
    if bundle_name == "whole_brain":
        builtin_descriptions["n_streamlines_" + bundle_name] =\
            f"Number of streamlines (uncleaned) identified as belonging to a bundle"
        builtin_descriptions["n_streamlines_clean_" + bundle_name] =\
            f"Number of streamlines (cleaned) identified as belonging to a bundle"
    else:
        builtin_descriptions["n_streamlines_" + bundle_name] =\
            f"Number of streamlines (uncleaned) found for bundle: {bundle_name}"
        builtin_descriptions["n_streamlines_clean_" + bundle_name] =\
            f"Number of streamlines (cleaned) found for bundle: {bundle_name}"
