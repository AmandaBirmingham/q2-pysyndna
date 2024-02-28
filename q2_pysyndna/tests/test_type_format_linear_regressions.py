from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_pysyndna import (
    __package_name__, LinearRegressionsYamlFormat,
    LinearRegressionsDirectoryFormat, LinearRegressions)
from q2_pysyndna._type_format_linear_regressions import (
    load_and_validate_linearregressionsyaml_fp,
    fill_linearregressionsyamlformat)


class TestLinearRegressionsTypes(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_linear_regressions_semantic_types_registration(self):
        self.assertRegisteredSemanticType(LinearRegressions)
        self.assertSemanticTypeRegisteredToFormat(
            LinearRegressions,
            LinearRegressionsDirectoryFormat)


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


class TestLinearRegressionsHelpers(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_load_and_validate_linearregressionsyaml_fp_valid(self):
        rel_fps = ['linear_regressions/linear_regressions.yaml',
                   'linear_regressions_minimal/linear_regressions.yaml']
        abs_fps = [self.get_data_path(rel_fp)
                   for rel_fp in rel_fps]
        expected_dicts = \
            [{
                'example1': {'intercept': -6.77539505390338,
                             'intercept_stderr': 0.2361976278251443,
                             'pvalue': 1.428443560659758e-07,
                             'rvalue': 0.9865030975156575,
                             'slope': 1.24487652379132,
                             'stderr': 0.07305408550335003},
                'example2': {'intercept': -7.155318973708384,
                             'intercept_stderr': 0.2563956755844754,
                             'pvalue': 1.505381146809759e-07,
                             'rvalue': 0.9863241797356326,
                             'slope': 1.24675913604407,
                             'stderr': 0.07365795255302438},
                'example3': None},
            {
                'example1': {'intercept': -6.77539505390338,
                             'intercept_stderr': 0.2361976278251443,
                             'pvalue': 1.428443560659758e-07,
                             'rvalue': 0.9865030975156575,
                             'slope': 1.24487652379132,
                             'stderr': 0.07305408550335003}
            }]

        for i in range(len(abs_fps)):
            abs_fp = abs_fps[i]
            out_dict = load_and_validate_linearregressionsyaml_fp(abs_fp)
            self.assertEqual(expected_dicts[i], out_dict)

    def test_load_and_validate_linearregressionsyaml_fp_empty_err(self):
        test_fp = self.get_data_path(
            'linear_regressions_minimal/linear_regressions.log')
        with self.assertRaisesRegex(
                ValidationError,
                r"Expected at least one regression, but got none"):
            _ = load_and_validate_linearregressionsyaml_fp(test_fp)

    def test_load_and_validate_linearregressionsyaml_fp_notdict_err(self):
        test_fp = self.get_data_path(
            'linear_regressions/linear_regressions.log')
        with self.assertRaisesRegex(
                ValidationError,
                r"Expected a dictionary, but got"):
            _ = load_and_validate_linearregressionsyaml_fp(test_fp)

    def test_load_and_validate_linearregressionsyaml_fp_malformed1_err(self):
        # top-level values must be null or a dict
        test_fp = self.get_data_path(
            'linear_regressions_malformed_1.yaml')
        with self.assertRaisesRegex(
                ValidationError,
                r"Expected None or a dictionary of regression "
                r"information as the value of the key"):
            _ = load_and_validate_linearregressionsyaml_fp(test_fp)

    def test_load_and_validate_linearregressionsyaml_fp_malformed2_err(self):
        # missing key "intercept_stderr"
        test_fp = self.get_data_path(
            'linear_regressions_malformed_2.yaml')
        with self.assertRaisesRegex(
                ValidationError,
                r"Expected regression for example1 to include the following "
                r"required keys: \{'intercept_stderr'\}"):
            _ = load_and_validate_linearregressionsyaml_fp(test_fp)

    def test_load_and_validate_linearregressionsyaml_fp_malformed3_err(self):
        # linear regression field values must be floats
        test_fp = self.get_data_path(
            'linear_regressions_malformed_3.yaml')
        with self.assertRaisesRegex(
                ValidationError,
                r"Expected a float as the value of the regression "
                r"information key"):
            _ = load_and_validate_linearregressionsyaml_fp(test_fp)

    def test_fill_linearregressionsyamlformat_w_format_input(self):
        test_format = LinearRegressionsYamlFormat()
        test_dict = {
                'example1': {'intercept': -6.77539505390338,
                             'intercept_stderr': 0.2361976278251443,
                             'pvalue': 1.428443560659758e-07,
                             'rvalue': 0.9865030975156575,
                             'slope': 1.24487652379132,
                             'stderr': 0.07305408550335003},
                'example2': {'intercept': -7.155318973708384,
                             'intercept_stderr': 0.2563956755844754,
                             'pvalue': 1.505381146809759e-07,
                             'rvalue': 0.9863241797356326,
                             'slope': 1.24675913604407,
                             'stderr': 0.07365795255302438},
                'example3': None}
        expected_contents = """example1:
  intercept: -6.77539505390338
  intercept_stderr: 0.2361976278251443
  pvalue: 1.428443560659758e-07
  rvalue: 0.9865030975156575
  slope: 1.24487652379132
  stderr: 0.07305408550335003
example2:
  intercept: -7.155318973708384
  intercept_stderr: 0.2563956755844754
  pvalue: 1.505381146809759e-07
  rvalue: 0.9863241797356326
  slope: 1.24675913604407
  stderr: 0.07365795255302438
example3: null
"""

        # ensure the existing format is filled with the expected contents
        _ = fill_linearregressionsyamlformat(test_dict, test_format)

        with test_format.open() as fh:
            self.assertEqual(fh.read(), expected_contents)