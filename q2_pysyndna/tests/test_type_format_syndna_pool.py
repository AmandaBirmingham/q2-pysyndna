import pandas
from pandas.testing import assert_frame_equal
from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_pysyndna import (
    __package_name__, SyndnaPoolCsvFormat,
    SyndnaPoolDirectoryFormat, SyndnaPoolConcentrationTable)
from q2_pysyndna._type_format_syndna_pool import \
    syndna_pool_csv_format_to_df, SYNDNA_ID_KEY, SYNDNA_INDIV_NG_UL_KEY


class TestSyndnaPoolConcentrationTableTypes(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_syndna_pool_semantic_types_registration(self):
        self.assertRegisteredSemanticType(SyndnaPoolConcentrationTable)
        self.assertSemanticTypeRegisteredToFormat(
            SyndnaPoolConcentrationTable,
            SyndnaPoolDirectoryFormat)


class TestSyndnaPoolCsvFormat(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_syndna_pool_csv_format_valid(self):
        filenames = ['syndna_pool.csv',
                     'syndna_pool_with_comments.csv']
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            test_format = SyndnaPoolCsvFormat(filepath, mode='r')
            test_format.validate()

    def test_syndna_pool_csv_format_invalid(self):
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


class TestSyndnaPoolCsvFormatTransformers(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_syndna_pool_csv_format_to_df(self):
        expected_dict = {SYNDNA_ID_KEY: [
            "p126", "p136", "p146", "p156", "p166", "p226", "p236", "p246",
            "p256", "p266"],
            SYNDNA_INDIV_NG_UL_KEY: [
                1, 0.1, 0.01, 0.001, 0.0001, 0.0001, 0.001, 0.01, 0.1, 1]}
        expected_df = pandas.DataFrame(expected_dict)

        filenames = ['syndna_pool.csv',
                     'syndna_pool_with_comments.csv']
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            obs_df = syndna_pool_csv_format_to_df(
                SyndnaPoolCsvFormat(filepath, mode='r'))
            assert_frame_equal(expected_df, obs_df)
