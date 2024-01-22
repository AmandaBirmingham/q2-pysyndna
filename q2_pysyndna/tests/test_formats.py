
from q2_pysyndna import (
    __package_name__, SyndnaPoolCsvFormat, LinearRegressionsYamlFormat,
    LinearRegressionsLogFormat, LinearRegressionsDirectoryFormat
)
from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase


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


class TestLinearRegressionsYamlFormat(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_linearregressionyaml_format_valid(self):
        filenames = ['linear_regressions/linear_regressions.yaml',
                     'linear_regressions_minimal/linear_regressions.yaml']
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            test_format = LinearRegressionsYamlFormat(filepath, mode='r')
            test_format.validate()

    def test_linearregressionyaml_format_invalid(self):
        filenames = [
            # empty
            'linear_regressions_minimal/linear_regressions.log',
            # not a dictionary--just text
            'linear_regressions/linear_regressions.log',
            # top-level values must be null or a dict
            'linear_regressions_malformed_1.yaml',
            # missing key "intercept_stderr"
            'linear_regressions_malformed_2.yaml',
            # linear regression field values must be floats
            'linear_regressions_malformed_3.yaml'
        ]
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            with self.assertRaisesRegex(ValidationError, r'Expected '):
                test_format = LinearRegressionsYamlFormat(filepath, mode='r')
                test_format.validate()


class TestLinearRegressionsLogFormat(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_linearregressionlog_format_valid(self):
        filenames = ['linear_regressions/linear_regressions.log',
                     'linear_regressions_minimal/linear_regressions.log']
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            test_format = LinearRegressionsLogFormat(filepath, mode='r')
            test_format.validate()

    def test_linearregressionlog_format_invalid(self):
        made_up_path = self.get_data_path('made_up_filename')
        with self.assertRaisesRegex(ValidationError, r'is not a file.'):
            test_format = LinearRegressionsLogFormat(made_up_path, mode='r')
            test_format.validate()


class TestLinearRegressionsDirectoryFormat(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_linearregressiondirectory_format_valid(self):
        rel_fps = ['linear_regressions',
                   'linear_regressions_minimal']
        abs_fps = [self.get_data_path(rel_fp)
                   for rel_fp in rel_fps]

        for abs_fp in abs_fps:
            test_format = LinearRegressionsDirectoryFormat(abs_fp, mode='r')
            test_format.validate()

    def test_linearregressiondirectory_format_invalid(self):
        rel_fps = ['linear_regressions_wo_log',
                   'linear_regressions_wo_yaml']
        abs_fps = [self.get_data_path(rel_fp)
                   for rel_fp in rel_fps]

        for abs_fp in abs_fps:
            with self.assertRaisesRegex(
                    ValidationError,  r'Missing one or more files'):
                test_format = LinearRegressionsDirectoryFormat(
                    abs_fp, mode='r')
                test_format.validate()
