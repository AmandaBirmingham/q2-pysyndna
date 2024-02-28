from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_pysyndna import (
    __package_name__, SyndnaPoolCsvFormat,
    SyndnaPoolDirectoryFormat, SyndnaPoolConcentrationTable)


class TestSyndnaPoolConcentrationTableTypes(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_syndna_pool_semantic_types_registration(self):
        self.assertRegisteredSemanticType(SyndnaPoolConcentrationTable)
        self.assertSemanticTypeRegisteredToFormat(
            SyndnaPoolConcentrationTable,
            SyndnaPoolDirectoryFormat)


class TestSyndnaPoolCsvFormat(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_syndnapoolcsv_format_valid(self):
        filenames = ['syndna_pool.csv',
                     'syndna_pool_with_comments.csv']
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            test_format = SyndnaPoolCsvFormat(filepath, mode='r')
            test_format.validate()

    def test_syndnapoolcsv_format_invalid(self):
        filenames = ['syndna_pool_wo_correct_cols.csv',
                     'syndna_pool_wo_data.csv',
                     'syndna_pool_wo_header.csv']
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            with self.assertRaisesRegex(ValidationError, r'Expected '):
                test_format = SyndnaPoolCsvFormat(filepath, mode='r')
                test_format.validate()

# NB: No tests for SyndnaPoolDirectoryFormat because it's a single-file one
