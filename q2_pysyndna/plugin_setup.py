import biom
import pandas
from typing import Dict, Union, List
from qiime2.plugin import (Plugin, Int, Float, Range, Str, Choices,
                           Metadata, Citations)
from q2_types.feature_table import (FeatureTable, Frequency)
from q2_types.feature_data import FeatureData

from pysyndna import OGU_CELLS_PER_G_OF_GDNA_KEY, OGU_CELLS_PER_G_OF_SAMPLE_KEY
import q2_pysyndna
from q2_pysyndna._type_format_syndna_pool import (
    SyndnaPoolConcentrationTable,
    SyndnaPoolCsvFormat, SyndnaPoolDirectoryFormat)
from q2_pysyndna._type_format_linear_regressions import (
    LinearRegressionsObjects, LinearRegressions,
    LinearRegressionsYamlFormat, LinearRegressionsDirectoryFormat,
    load_and_validate_linearregressionsyaml_fp,
    fill_linearregressionsyamlformat)
from q2_pysyndna._type_format_pysyndna_log import (
    PysyndnaLog,
    PysyndnaLogFormat, PysyndnaLogDirectoryFormat,
    fill_pysyndnalogformat, load_list_from_pysyndnalog_fp,
    extract_list_from_pysyndnalogdir_format)
from q2_pysyndna._type_format_length import (
    Length,
    TSVLengthFormat, TSVLengthDirectoryFormat,
    tsvlength_fp_to_dataframe,
    dataframe_to_tsvlength_format)
from q2_pysyndna._type_format_coords import (
    Coords,
    CoordsFormat, CoordsDirectoryFormat,
    coords_fp_to_dataframe,
    dataframe_to_coords_format
)

plugin = Plugin(
    name=q2_pysyndna.__plugin_name__,
    version=q2_pysyndna.__version__,
    website=q2_pysyndna.__url__,
    package=q2_pysyndna.__package_name__,
    citations=Citations.load(
        q2_pysyndna.__citations_fname__, package=q2_pysyndna.__package_name__),
    description=q2_pysyndna.__long_description__,
    short_description=q2_pysyndna.__description__,
)

plugin.register_semantic_types(SyndnaPoolConcentrationTable)
plugin.register_formats(SyndnaPoolCsvFormat, SyndnaPoolDirectoryFormat)
plugin.register_semantic_type_to_format(
    SyndnaPoolConcentrationTable, SyndnaPoolDirectoryFormat)

plugin.register_semantic_types(LinearRegressions)
plugin.register_formats(
    LinearRegressionsYamlFormat,
    LinearRegressionsDirectoryFormat)
plugin.register_semantic_type_to_format(
    LinearRegressions, LinearRegressionsDirectoryFormat)

plugin.register_semantic_types(PysyndnaLog)
plugin.register_formats(PysyndnaLogFormat, PysyndnaLogDirectoryFormat)
plugin.register_semantic_type_to_format(
    PysyndnaLog, PysyndnaLogDirectoryFormat)

plugin.register_semantic_types(Length)
plugin.register_formats(TSVLengthFormat, TSVLengthDirectoryFormat)
plugin.register_artifact_class(
    FeatureData[Length],
    directory_format=TSVLengthDirectoryFormat,
    description="Integer lengths associated with a set of features.")

plugin.register_semantic_types(Coords)
plugin.register_formats(CoordsFormat, CoordsDirectoryFormat)
plugin.register_artifact_class(
    FeatureData[Coords],
    directory_format=CoordsDirectoryFormat,
    description="Integer start and end positions associated with "
                "a set of features.")


@plugin.register_transformer
def _syndnapoolcsv_to_df(ff: SyndnaPoolCsvFormat) -> pandas.DataFrame:
    result = pandas.read_csv(str(ff), header=0, comment='#')
    return result


@plugin.register_transformer
def _typingdict_to_linearregyaml(
        data: Dict[str, Union[Dict[str, float], None]]) -> \
        LinearRegressionsYamlFormat:
    ff = fill_linearregressionsyamlformat(data)
    return ff


@plugin.register_transformer
def _dict_to_linearregyaml(data: dict) -> LinearRegressionsYamlFormat:
    ff = fill_linearregressionsyamlformat(data)
    return ff


@plugin.register_transformer
def _LinearRegressionsYamlFormat_to_dict(
        data: LinearRegressionsYamlFormat) -> dict:
    return load_and_validate_linearregressionsyaml_fp(str(data))


@plugin.register_transformer
def _list_to_pysyndnalog(data: list) -> PysyndnaLogFormat:
    ff = fill_pysyndnalogformat(data)
    return ff


@plugin.register_transformer
def _pysyndnalog_to_list(data: PysyndnaLogFormat) -> List[str]:
    return load_list_from_pysyndnalog_fp(data)


@plugin.register_transformer
def _typinglist_to_pysyndnalog(data: List[str]) -> PysyndnaLogFormat:
    ff = fill_pysyndnalogformat(data)
    return ff


@plugin.register_transformer
def _pysyndnalogdir_to_list(data: PysyndnaLogDirectoryFormat) -> list:
    return extract_list_from_pysyndnalogdir_format(data)


@plugin.register_transformer
def _linearregobjs_to_linearregsdir(data: LinearRegressionsObjects) -> \
        LinearRegressionsDirectoryFormat:
    fy = fill_linearregressionsyamlformat(data.linregs_dict)
    fl = fill_pysyndnalogformat(data.log_msgs_list)

    ff = LinearRegressionsDirectoryFormat()
    ff.linregs_yaml.write_data(fy, LinearRegressionsYamlFormat)
    ff.log.write_data(fl, PysyndnaLogFormat)
    return ff


@plugin.register_transformer
def _format_tuple_to_linearregsdir(
        data: (LinearRegressionsYamlFormat, PysyndnaLogFormat)) -> \
        LinearRegressionsDirectoryFormat:
    ff = LinearRegressionsDirectoryFormat()

    fy = fill_linearregressionsyamlformat(data.linregs_dict)
    fl = fill_pysyndnalogformat(data.log_msgs_list)
    return ff


@plugin.register_transformer
def _linearregsdir_to_linearregobjs(
        data: LinearRegressionsDirectoryFormat) -> LinearRegressionsObjects:
    linregs_dict = load_and_validate_linearregressionsyaml_fp(
        data.linregs_yaml)
    log_msgs_list = load_list_from_pysyndnalog_fp(data.log)
    result = LinearRegressionsObjects(linregs_dict, log_msgs_list)
    return result


@plugin.register_transformer
def _tsvlen_to_df(ff: TSVLengthFormat) -> pandas.DataFrame:
    # validate the dataframe and convert lengths to integers
    df = tsvlength_fp_to_dataframe(str(ff))
    return df


@plugin.register_transformer
def _df_to_tsvlen(df: pandas.DataFrame) -> TSVLengthFormat:
    return dataframe_to_tsvlength_format(df)


@plugin.register_transformer
def _coords_to_df(ff: CoordsFormat) -> pandas.DataFrame:
    # validate the dataframe and convert coords to integers
    df = coords_fp_to_dataframe(str(ff))
    return df


@plugin.register_transformer
def _df_to_coords(df: pandas.DataFrame) -> CoordsFormat:
    return dataframe_to_coords_format(df)


plugin.methods.register_function(
    function=q2_pysyndna.fit,
    name='Fit linear regression models.',
    description=(
        'Fit per-sample linear regression models predicting input mass from '
        'read counts using synDNA spike-ins'),
    inputs={'syndna_concs': SyndnaPoolConcentrationTable,
            'syndna_counts': FeatureTable[Frequency]},
    input_descriptions={
        'syndna_concs': "Syndna pool(s)' membership and concentrations.",
        'syndna_counts': 'Feature table of syndna counts.'},
    parameters={
        'metadata': Metadata,
        'min_sample_count': Int % Range(1, None)},
    parameter_descriptions={
        'metadata': 'Metadata file with sample information.',
        'min_sample_count': 'Minimum number of counts required for a sample '
                            'to be included in the regression.  Samples with '
                            'fewer counts will be excluded.'},
    outputs=[('regression_models', LinearRegressions)],
    output_descriptions={
        'regression_models': 'Linear regression models trained for each '
                             'qualifying sample, and log messages from the '
                             'regression fitting process.'}
)

plugin.methods.register_function(
    function=q2_pysyndna.count_cells,
    name='Calculate cell counts.',
    description=(
        'Calculate number of cells of each OGU per gram of sample using '
        'per-sample linear regression models based on synDNA spike-ins'),
    inputs={'regression_models': LinearRegressions,
            'ogu_counts': FeatureTable[Frequency],
            'ogu_lengths': FeatureData[Length]},
    input_descriptions={
        'regression_models': 'Linear regression models trained for each '
                             'qualifying sample.',
        'ogu_counts': 'Feature table of OGU counts.',
        'ogu_lengths': 'Lengths of OGUs.'},
    parameters={
        'metadata': Metadata,
        'read_length': Int % Range(1, None),
        'min_percent_coverage': Float % Range(1, None),
        'min_rsquared': Float % Range(0, 1),
        'output_metric': Str % Choices(OGU_CELLS_PER_G_OF_GDNA_KEY,
                                       OGU_CELLS_PER_G_OF_SAMPLE_KEY)},
    parameter_descriptions={
        'metadata': 'Metadata file with sample information.',
        'read_length': 'Length of reads in basepairs (usually but not '
                       'always 150).',
        'min_percent_coverage': 'Minimum allowable percent coverage of an '
                                'OGU in a sample needed to include that '
                                'OGU/sample in the output.',
        'min_rsquared': 'Minimum allowable R^2 value for the linear regression'
                        ' model for a sample needed to include that sample in '
                        'the output.',
        'output_metric': 'The metric to calculate and output.  '
                         f'Choices are {OGU_CELLS_PER_G_OF_GDNA_KEY} and '
                         f'{OGU_CELLS_PER_G_OF_SAMPLE_KEY}.'},
    outputs=[('cell_counts', FeatureTable[Frequency]),
             ('cell_count_log', PysyndnaLog)],
    output_descriptions={
        'cell_counts': 'Cell counts per OGU per sample.',
        'cell_count_log': 'Log messages from the cell count calculation '
                          'process.'}
)


plugin.methods.register_function(
    function=q2_pysyndna.count_copies,
    name='Calculate copies of RNA of each OGU+ORF.',
    description=(
        'Calculate number of copies of RNA of each OGU+ORF '
        '(each ORF on each OGU) per gram of sample.'),
    inputs={'ogu_orf_counts': FeatureTable[Frequency],
            'ogu_orf_coords': FeatureData[Coords]},
    input_descriptions={
        'ogu_orf_counts': 'Feature table of OGU+ORF counts.',
        'ogu_orf_coords': 'Start and end coordinates of OGU+ORFs.'},
    parameters={'metadata': Metadata},
    parameter_descriptions={
        'metadata': 'Metadata file with sample information.'},
    outputs=[('copy_counts', FeatureTable[Frequency]),
             ('copy_count_log', PysyndnaLog)],
    output_descriptions={
        'copy_counts': 'RNA copy counts per OGU+ORF per sample.',
        'copy_count_log': 'Log messages from the copy count calculation '
                          'process.'}
)

plugin.visualizers.register_function(
    function=q2_pysyndna.view_fit,
    name='Visualize linear regression results.',
    description='Visualize linear regression model results and log messages '
                'from a pysyndna fit process.',
    inputs={'linear_regressions': LinearRegressions},
    input_descriptions={
        'linear_regressions': 'Results of a pysyndna fit process.'},
    parameters={},
)

plugin.visualizers.register_function(
    function=q2_pysyndna.view_log,
    name='Visualize log messages.',
    description='Visualize log messages from a pysyndna process.',
    inputs={'log': PysyndnaLog},
    input_descriptions={'log': 'Log messages from a pysyndna process.'},
    parameters={},
)
