from __future__ import annotations

import pandas
import pysyndna
import biom
from qiime2.plugin import Metadata


# NB: Because there is a transformer on the plugin that can turn a
# SyndnaPoolConcentrationTable (which is what the plugin gets as its first
# argument) into a pandas.DataFrame, that transformation will be done
# automagically and this will receive a pandas.DataFrame as its first argument.
def fit(syndna_concs: pandas.DataFrame,
        syndna_counts: biom.Table,
        metadata: Metadata,
        min_sample_count: int = 1) -> \
        (dict[str, dict[str, float] | None], list[str]):
    """Fit linear regression models predicting input mass from read counts.

    Parameters
    ----------
    syndna_concs : SyndnaPoolConcentrationTable
        Table of syndna ids in pool and the concentration of each.
    syndna_counts : biom.Table
        Feature table of syndna counts.
    metadata : Metadata
        Metadata file with sample information.
    min_sample_count : int, optional
        Minimum number of counts required for a sample to be included in the
        regression.  Samples with fewer counts will be excluded.

    Returns
    -------
    linear_regressions_dict :  dict[str, dict[str, float] | None]
        Dictionary keyed by sample id, containing for each sample either None
        (if no model could be trained for that SAMPLE_ID_KEY) or a dictionary
        representation of the sample's LinregressResult, with each property
        name as a key and that property's value as the value, as a float.
    log_messages_list : list[str]
        List of log messages generated during the fitting process.
    """

    # convert input biom table to a pd.SparseDataFrame, which is should act
    # basically like a pd.DataFrame but take up less memory
    reads_per_syndna_per_sample_df = syndna_counts.to_dataframe(dense=False)

    linregs_dict, log_msgs_list = pysyndna.fit_linear_regression_models(
        syndna_concs, metadata, reads_per_syndna_per_sample_df,
        min_sample_count)

    return linregs_dict, log_msgs_list
