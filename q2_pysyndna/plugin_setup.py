from __future__ import annotations

import pandas
import q2_pysyndna
from q2_pysyndna._formats_and_types import (
    SyndnaPoolCsvFormat,
    SyndnaPoolDirectoryFormat,
    SyndnaPoolConcentrationTable,
    LinearRegressionsYamlFormat, LinearRegressionsLogFormat,
    LinearRegressionsDirectoryFormat, LinearRegressions)

from q2_types.feature_table import (FeatureTable, Frequency)
from qiime2.plugin import (Plugin, Int, Range, Metadata, Citations)
import yaml


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

plugin.register_formats(SyndnaPoolCsvFormat, SyndnaPoolDirectoryFormat)
plugin.register_semantic_types(SyndnaPoolConcentrationTable)
plugin.register_semantic_type_to_format(
    SyndnaPoolConcentrationTable, SyndnaPoolDirectoryFormat)
plugin.register_formats(
    LinearRegressionsYamlFormat, LinearRegressionsLogFormat,
    LinearRegressionsDirectoryFormat)
plugin.register_semantic_types(LinearRegressions)
plugin.register_semantic_type_to_format(
    LinearRegressions, LinearRegressionsDirectoryFormat)


@plugin.register_transformer
def _1(ff: SyndnaPoolCsvFormat) -> pandas.DataFrame:
    result = pandas.read_csv(str(ff), header=0, comment='#')
    return result


@plugin.register_transformer
def _2(data: dict[str, dict[str, float] | None]) -> \
        LinearRegressionsYamlFormat:
    ff = LinearRegressionsYamlFormat()
    with ff.open() as fh:
        yaml.safe_dump(data, fh)
    return ff


@plugin.register_transformer
def _3(data: list[str]) -> LinearRegressionsLogFormat:
    data_str = '\n'.join(data)
    ff = LinearRegressionsLogFormat()
    with ff.open() as fh:
        fh.write(data_str)
    return ff


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
                             'qualifying sample.'}
)

