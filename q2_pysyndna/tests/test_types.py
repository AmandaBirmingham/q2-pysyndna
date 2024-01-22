from q2_pysyndna import (
    SyndnaPoolConcentrationTable, LinearRegressions,
    SyndnaPoolDirectoryFormat, LinearRegressionsDirectoryFormat,
    __package_name__)  

from qiime2.plugin.testing import TestPluginBase


class TestTypes(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_syndna_pool_semantic_types_registration(self):
        self.assertRegisteredSemanticType(SyndnaPoolConcentrationTable)
        self.assertSemanticTypeRegisteredToFormat(
            SyndnaPoolConcentrationTable,
            SyndnaPoolDirectoryFormat)

    def test_linear_regressions_semantic_types_registration(self):
        self.assertRegisteredSemanticType(LinearRegressions)
        self.assertSemanticTypeRegisteredToFormat(
            LinearRegressions,
            LinearRegressionsDirectoryFormat)
