import biom
import pandas
from qiime2.plugin import Metadata

from pysyndna import fit_linear_regression_models, calc_ogu_cell_counts_biom, \
    calc_copies_of_ogu_orf_ssrna_per_g_sample_from_dfs, \
    OGU_CELLS_PER_G_OF_SAMPLE_KEY, OGU_ID_KEY, OGU_LEN_IN_BP_KEY
from q2_pysyndna._type_format_linear_regressions import \
    LinearRegressionsObjects


def _make_pysydna_metadata(metadata: pandas.DataFrame) -> pandas.DataFrame:
    metadata_df = metadata.to_dataframe()
    metadata_df.reset_index(inplace=True)
    return metadata_df


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

    metadata_df = _make_pysydna_metadata(metadata)

    # convert input biom table to a pd.SparseDataFrame, which is should act
    # basically like a pd.DataFrame but take up less memory
    reads_per_syndna_per_sample_df = syndna_counts.to_dataframe(dense=False)

    linregs_dict, log_msgs_list = fit_linear_regression_models(
        syndna_concs, metadata_df, reads_per_syndna_per_sample_df,
        min_sample_count)

    result = LinearRegressionsObjects(linregs_dict, log_msgs_list)
    return result


def count_cells(
        regression_models: LinearRegressionsObjects,
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

    metadata_df = _make_pysydna_metadata(metadata)

    ogu_lengths.index.name = OGU_ID_KEY
    ogu_lengths.columns = [OGU_LEN_IN_BP_KEY]

    cell_counts_biom, log_msgs_list = calc_ogu_cell_counts_biom(
        metadata_df, regression_models.linregs_dict, ogu_counts,
        ogu_lengths, read_length, min_percent_coverage, min_rsquared,
        output_metric)

    return cell_counts_biom, log_msgs_list


def count_copies(
        ogu_orf_counts: biom.Table,
        ogu_orf_coords: pandas.DataFrame,
        metadata: Metadata) -> \
        (biom.Table, list):

    """Calculate the copies of each OGU+ORF ssRNA per gram of sample.

    Parameters
    ----------
    ogu_orf_counts : biom.Table
        A biom.Table with the number of reads per OGU+ORF per sample, such
        as that output by woltka.
    ogu_orf_coords: pandas.DataFrame
        A DataFrame with columns for OGU_ORF_ID_KEY, OGU_ORF_START_KEY, and
        OGU_ORF_END_KEY.
    metadata : Metadata
        A Metadata object containing SAMPLE_ID_KEY as key and
        SAMPLE_IN_ALIQUOT_MASS_G_KEY, SSRNA_CONCENTRATION_NG_UL_KEY,
        ELUTE_VOL_UL_KEY, and TOTAL_BIOLOGICAL_READS_KEY.

    Returns
    -------
    copies_of_ogu_orf_ssrna_per_g_sample : biom.Table
        A biom.Table with the copies of each OGU+ORF ssRNA per gram of sample.
    log_msgs_list: list[str]
        A list of log messages, if any, generated during the function's
        operation.  Empty if no log messages were generated.
    """

    metadata_df = _make_pysydna_metadata(metadata)

    copies_of_ogu_orf_ssrna_per_g_sample, log_msgs_list = \
        calc_copies_of_ogu_orf_ssrna_per_g_sample_from_dfs(
            metadata_df,
            ogu_orf_counts,
            ogu_orf_coords)

    return copies_of_ogu_orf_ssrna_per_g_sample, log_msgs_list
