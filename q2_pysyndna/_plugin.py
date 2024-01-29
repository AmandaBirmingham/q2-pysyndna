import collections
import pandas
import pysyndna
import biom
from qiime2.plugin import Metadata


LinearRegressionsObjects = collections.namedtuple(
    "LinearRegressionsObjects",
    ["linregs_dict", "log_msgs_list"])


# NB: Because there is a transformer on the plugin that can turn a
# SyndnaPoolConcentrationTable (which is what the plugin gets as its first
# argument) into a pandas.DataFrame, that transformation will be done
# automagically and this will receive a pandas.DataFrame as its first argument.
def fit(syndna_concs: pandas.DataFrame,
        syndna_counts: biom.Table,
        metadata: Metadata,
        min_sample_count: int = 1) -> LinearRegressionsObjects:
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
    linear_regressions_objects_tuple: LinearRegressionsObjects
        Tuple of the linear regression models and the log messages generated
        during the fitting process. The linear regression models are a
        Dictionary keyed by sample id, containing for each sample either None
        (if no model could be trained for that SAMPLE_ID_KEY) or a dictionary
        representation of the sample's LinregressResult, with each property
        name as a key and that property's value as the value, as a float.
        The log messages are a list of log message strings generated during the
        fitting process.
    """

    # convert input biom table to a pd.SparseDataFrame, which is should act
    # basically like a pd.DataFrame but take up less memory
    reads_per_syndna_per_sample_df = syndna_counts.to_dataframe(dense=False)

    linregs_dict, log_msgs_list = pysyndna.fit_linear_regression_models(
        syndna_concs, metadata, reads_per_syndna_per_sample_df,
        min_sample_count)

    # # TODO: remove hardcoded test values after debugging complete
    # linregs_dict = {"example_test": {
    #     "slope": 1.24675913604407,
    #     "intercept": -7.155318973708384,
    #     "rvalue": 0.9863241797356326,
    #     "pvalue": 1.505381146809759e-07,
    #     "stderr": 0.07365795255302438,
    #     "intercept_stderr": 0.2563956755844754}}
    # log_msgs_list = ["test log message 1"]

    result = LinearRegressionsObjects(linregs_dict, log_msgs_list)
    return result
