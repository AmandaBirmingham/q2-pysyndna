import q2_pysyndna
from q2_pysyndna._formats_and_types import (
    SyndnaPoolsYamlFormat, LinearRegressionsYamlFormat,
    SyndnaPools, LinearRegressions)

from q2_types.feature_table import (FeatureTable, Frequency)
from qiime2.plugin import (Plugin, Int, Range, Metadata, Citations)

plugin = Plugin(
    name="pysyndna",
    version=q2_pysyndna.__version__,
    website=q2_pysyndna.__url__,
    package=q2_pysyndna.__package__,
    citations=Citations.load(
        'citations.bib', package=q2_pysyndna.__package__),
    description=q2_pysyndna.__long_description__,
    short_description=q2_pysyndna.__description__,
)

plugin.register_formats(SyndnaPoolsYamlFormat)
plugin.register_semantic_types(SyndnaPools)
plugin.register_semantic_type_to_format(SyndnaPools, SyndnaPoolsYamlFormat)

plugin.methods.register_function(
    function=q2_pysyndna.fit,
    name='Fit linear regression models.',
    description=(
        'Fit per-sample linear regression models predicting input mass from '
        'read counts using synDNA spike-ins'),
    inputs={'syndna_concs': SyndnaPools,
            'metadata': Metadata,
            'syndna_counts': FeatureTable[Frequency]},
    input_descriptions={
        'syndna_concs': "Syndna pool(s)' membership and concentrations.",
        'metadata': 'Metadata file with sample information.',
        'syndna_counts': 'Feature table of syndna counts.'},
    parameters={'min_sample_count': Int % Range(1, None)},
    parameter_descriptions={
        'min_sample_count': 'Minimum number of counts required for a sample '
                            'to be included in the regression.  Samples with '
                            'fewer counts will be excluded.'},
    outputs=[('regression_models', LinearRegressions)],
    output_descriptions={
        'regression_models': 'Linear regression models trained for each '
                             'qualifying sample.'}
)
