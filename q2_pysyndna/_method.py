import biom
import numpy as np
import pandas
from qiime2.plugin import Metadata

from pysyndna import OGU_CELLS_PER_G_OF_SAMPLE_KEY
from q2_pysyndna._type_format_linear_regressions import \
    LinearRegressionsObjects, LinearRegressionsDirectoryFormat


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
        A Metadata file with sample information.
    min_sample_count : int, optional
        Minimum number of counts required for a sample to be included in the
        regression.  Samples with fewer counts will be excluded.

    Returns
    -------
    linear_regressions_object: LinearRegressionsObjects
        Tuple of the linear regression models and the log messages generated
        during the fitting process. The linear regression models are a
        Dictionary keyed by sample id, containing for each sample either None
        (if no model could be trained for that SAMPLE_ID_KEY) or a dictionary
        representation of the sample's LinregressResult, with each property
        name as a key and that property's value as the value, as a float.
        The log messages are a list of log message strings generated during the
        fitting process.
    """

    # # TODO: put back real logic after debugging complete
    # # convert input biom table to a pd.SparseDataFrame, which is should act
    # # basically like a pd.DataFrame but take up less memory
    # reads_per_syndna_per_sample_df = syndna_counts.to_dataframe(dense=False)
    #
    # linregs_dict, log_msgs_list = pysyndna.fit_linear_regression_models(
    #     syndna_concs, metadata, reads_per_syndna_per_sample_df,
    #     min_sample_count)

    # # TODO: remove hardcoded test values after debugging complete
    linregs_dict = {"example_test": {
        "slope": 1.24675913604407,
        "intercept": -7.155318973708384,
        "rvalue": 0.9863241797356326,
        "pvalue": 1.505381146809759e-07,
        "stderr": 0.07365795255302438,
        "intercept_stderr": 0.2563956755844754}}
    log_msgs_list = ["test log message 1"]

    result = LinearRegressionsObjects(linregs_dict, log_msgs_list)
    return result


def calc_cell_counts(
        regression_models: LinearRegressionsDirectoryFormat,
        ogu_counts: biom.Table,
        ogu_lengths:  pandas.DataFrame,
        metadata: Metadata,
        read_length: int = 150,
        min_percent_coverage: float = 1,
        min_rsquared: float = 0.8,
        output_metric: str = OGU_CELLS_PER_G_OF_SAMPLE_KEY) -> \
        (biom.Table, list):

    """Calculate number of cells of each OGU per gram of sample.

    Parameters
    ----------
    regression_models : LinearRegressions
        Linear regression models trained for each qualifying sample, and logs.
    ogu_counts : biom.Table
        Feature table of OGU counts.
    ogu_lengths : pandas.DataFrame
        Lengths of OGUs.
    metadata : Metadata
        A Metadata file with sample information.
    read_length : int
        Length of reads in basepairs (usually but not necessarily the same as
        the length of the OGUs).
    min_percent_coverage : float
        Minimum percent coverage of the OGUs by reads required for a sample to
        be included in the regression.
    min_rsquared : float
        Minimum r-squared value required for a sample to be included in the
        regression.
    output_metric : str
        The metric to output. One of OGU_CELLS_PER_G_OF_GDNA_KEY or
        OGU_CELLS_PER_G_OF_SAMPLE_KEY.

    Returns
    -------
    cell_counts_objects_tuple: CellCountsObjects
        Tuple of cell counts and the log messages generated during the
        calculation process. The cell counts are a biom.Table of cell counts
        per gram for each OGU in each sample. The log messages are a list of
        log message strings generated during the calculation process.
    """

    # TODO: put back real functioning logic after debugging complete
    # cell_counts_biom, log_msgs_list = pysyndna.calc_ogu_cell_counts_biom(
    #     regression_models.linregs_dict, metadata, ogu_counts,
    #     ogu_lengths, read_length, min_percent_coverage, min_rsquared,
    #     output_metric)

    # TODO: remove hardcoded test values after debugging complete
    sample_ids = ["example1", "example4"]
    ogu_cell_counts_per_g_sample = np.array([
        [157373183.3914873, 23597204.3149076],
        [51026330.8697321, 134672840.2210325],
        [41099206.6945521, 0],
        [378706815.3787082, 56777764.5887874],
        [80657360.0375914, 12008439.3369959],
        [66764001.1050239, 9985433.5965833],
        [78187617.9691203, 0],
        [91085928.0975326, 13631697.3528372],
        [199150566.7379318, 29865774.0278729],
        [83241001.9519951, 12452394.7533948],
        [41754672.7649972, 6239881.9809863],
        [92468147.5568761, 13848368.6486051],
        [41072627.7089503, 6138060.2138924]])

    ogu_ids = [
        'Escherichia coli', 'Fusobacterium periodonticum',
        'Haemophilus influenzae', 'Lactobacillus gasseri',
        'Leptolyngbya valderiana', 'Neisseria flavescens',
        'Neisseria subflava', 'Prevotella sp. oral taxon 299',
        'Ruminococcus albus', 'Streptococcus mitis',
        'Streptococcus pneumoniae', 'Tyzzerella nexilis',
        'Veillonella dispar']

    cell_counts_biom = biom.table.Table(
        ogu_cell_counts_per_g_sample,
        ogu_ids,
        sample_ids)

    log_msgs_list = ["test log message 1", "test log message 2"]

    return cell_counts_biom, log_msgs_list
