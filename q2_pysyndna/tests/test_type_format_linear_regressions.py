from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_pysyndna import (
    __package_name__, LinearRegressionsYamlFormat,
    LinearRegressionsDirectoryFormat, LinearRegressions)
from q2_pysyndna._type_format_pysyndna_log import (
    extract_fp_from_directory_format)
from q2_pysyndna._type_format_linear_regressions import (
    LinearRegressionsObjects,
    yaml_fp_to_linear_regressions_yaml_format,
    dict_to_linear_regressions_yaml_format,
    linear_regressions_directory_format_to_linear_regressions_objects,
    linear_regressions_objects_to_linear_regressions_directory_format)


class TestLinearRegressionsTypes(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_linear_regressions_semantic_types_registration(self):
        self.assertRegisteredSemanticType(LinearRegressions)
        self.assertSemanticTypeRegisteredToFormat(
            LinearRegressions,
            LinearRegressionsDirectoryFormat)


class TestLinearRegressionsYamlFormat(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_linear_regressions_yaml_format_valid(self):
        filenames = ['linear_regressions/linear_regressions.yaml',
                     'linear_regressions_minimal/linear_regressions.yaml']
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            test_format = LinearRegressionsYamlFormat(filepath, mode='r')
            test_format.validate()

    def test_linear_regressions_yaml_format_invalid(self):
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

    def test_linear_regressions_directory_format_valid(self):
        rel_fps = ['linear_regressions',
                   'linear_regressions_minimal']
        abs_fps = [self.get_data_path(rel_fp)
                   for rel_fp in rel_fps]

        for abs_fp in abs_fps:
            test_format = LinearRegressionsDirectoryFormat(abs_fp, mode='r')
            test_format.validate()

    def test_linear_regressions_directory_format_invalid(self):
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


class TestLinearRegressionsTransformers(TestPluginBase):
    package = f'{__package_name__}.tests'

    TEST_DICT_1 = {
        'example1': {'intercept': -6.77539505390338,
                     'intercept_stderr': 0.2361976278251443,
                     'pvalue': 1.428443560659758e-07,
                     'rvalue': 0.9865030975156575,
                     'slope': 1.24487652379132,
                     'stderr': 0.07305408550335003}}

    TEST_DICT_2_3 = {
        'example2': {'intercept': -7.155318973708384,
                     'intercept_stderr': 0.2563956755844754,
                     'pvalue': 1.505381146809759e-07,
                     'rvalue': 0.9863241797356326,
                     'slope': 1.24675913604407,
                     'stderr': 0.07365795255302438},
        'example3': None}

    TEST_DICT_1_2_3 = {**TEST_DICT_1, **TEST_DICT_2_3}

    YAML_1 = """example1:
  intercept: -6.77539505390338
  intercept_stderr: 0.2361976278251443
  pvalue: 1.428443560659758e-07
  rvalue: 0.9865030975156575
  slope: 1.24487652379132
  stderr: 0.07305408550335003"""

    YAML_2_3 = """example2:
  intercept: -7.155318973708384
  intercept_stderr: 0.2563956755844754
  pvalue: 1.505381146809759e-07
  rvalue: 0.9863241797356326
  slope: 1.24675913604407
  stderr: 0.07365795255302438
example3: null
"""

    YAML_1_2_3 = f"{YAML_1}\n{YAML_2_3}"

    LINREGOBJ_1_2_3 = LinearRegressionsObjects(
        linregs_dict=TEST_DICT_1_2_3,
        log_msgs_list=["The following syndnas were dropped because they had fewer "
         "than 200 total reads aligned:['p166']"])

    @staticmethod
    def compare_linear_regressions_directory_formats(
            expected_format, out_format):
        for attr in ['linregs_yaml', 'log']:
            expected_fp = extract_fp_from_directory_format(
                expected_format, getattr(expected_format, attr))
            out_fp = extract_fp_from_directory_format(
                out_format, getattr(out_format, attr))
            with open(expected_fp) as fh:
                expected_text = fh.read().strip()
            with open(out_fp) as fi:
                out_text = fi.read().strip()
            yield expected_text, out_text.replace('"', "")

    def test_yaml_fp_to_linear_regressions_yaml_format_valid(self):
        rel_fps = ['linear_regressions/linear_regressions.yaml',
                   'linear_regressions_minimal/linear_regressions.yaml']
        abs_fps = [self.get_data_path(rel_fp)
                   for rel_fp in rel_fps]
        expected_dicts = \
            [self.TEST_DICT_1_2_3, self.TEST_DICT_1]

        for i in range(len(abs_fps)):
            abs_fp = abs_fps[i]
            out_dict = yaml_fp_to_linear_regressions_yaml_format(abs_fp)
            self.assertEqual(expected_dicts[i], out_dict)

    def test_yaml_fp_to_linear_regressions_yaml_format_err_empty(self):
        test_fp = self.get_data_path(
            'linear_regressions_minimal/linear_regressions.log')
        with self.assertRaisesRegex(
                ValidationError,
                r"Expected at least one regression, but got none"):
            _ = yaml_fp_to_linear_regressions_yaml_format(test_fp)

    def test_yaml_fp_to_linear_regressions_yaml_format_err_notdict(self):
        test_fp = self.get_data_path(
            'linear_regressions/linear_regressions.log')
        with self.assertRaisesRegex(
                ValidationError,
                r"Expected a dictionary, but got"):
            _ = yaml_fp_to_linear_regressions_yaml_format(test_fp)

    def test_yaml_fp_to_linear_regressions_yaml_format_err_malformed1(self):
        # top-level values must be null or a dict
        test_fp = self.get_data_path(
            'linear_regressions_malformed_1.yaml')
        with self.assertRaisesRegex(
                ValidationError,
                r"Expected None or a dictionary of regression "
                r"information as the value of the key"):
            _ = yaml_fp_to_linear_regressions_yaml_format(test_fp)

    def test_yaml_fp_to_linear_regressions_yaml_format_err_malformed2(self):
        # missing key "intercept_stderr"
        test_fp = self.get_data_path(
            'linear_regressions_malformed_2.yaml')
        with self.assertRaisesRegex(
                ValidationError,
                r"Expected regression for example1 to include the following "
                r"required keys: \{'intercept_stderr'\}"):
            _ = yaml_fp_to_linear_regressions_yaml_format(test_fp)

    def test_yaml_fp_to_linear_regressions_yaml_format_err_malformed3(self):
        # linear regression field values must be floats
        test_fp = self.get_data_path(
            'linear_regressions_malformed_3.yaml')
        with self.assertRaisesRegex(
                ValidationError,
                r"Expected a float as the value of the regression "
                r"information key"):
            _ = yaml_fp_to_linear_regressions_yaml_format(test_fp)

    def test_dict_to_linear_regressions_yaml_format_w_format_input(self):
        test_format = LinearRegressionsYamlFormat()

        # ensure the existing format is filled with the expected contents
        _ = dict_to_linear_regressions_yaml_format(
            self.TEST_DICT_1_2_3, test_format)

        with test_format.open() as fh:
            self.assertEqual(fh.read(), self.YAML_1_2_3)

    def test_dict_to_linear_regressions_yaml_format_wo_format_input(self):
        # ensure a new format is filled with the expected contents
        out_format = dict_to_linear_regressions_yaml_format(
            self.TEST_DICT_1_2_3)

        with out_format.open() as fh:
            self.assertEqual(fh.read(), self.YAML_1_2_3)

    def test_linear_regressions_directory_format_to_linear_regressions_objects(
            self):
        rel_fps = ['linear_regressions',
                   'linear_regressions_minimal']
        abs_fps = [self.get_data_path(rel_fp)
                   for rel_fp in rel_fps]

        expected_objs = [
            LinearRegressionsObjects(
                self.TEST_DICT_1_2_3,
                ["The following syndnas were dropped because they had fewer "
                 "than 200 total reads aligned:['p166']"]),
            LinearRegressionsObjects(
                self.TEST_DICT_1,
                [])]

        for i in range(len(abs_fps)):
            abs_fp = abs_fps[i]
            expected_obj = expected_objs[i]
            test_format = LinearRegressionsDirectoryFormat(abs_fp, mode='r')
            out_obj = linear_regressions_directory_format_to_linear_regressions_objects(test_format)
            self.assertDictEqual(
                expected_obj.linregs_dict, out_obj.linregs_dict)
            self.assertListEqual(
                expected_obj.log_msgs_list, out_obj.log_msgs_list)

    def test_linear_regressions_objects_to_linear_regressions_directory_format(
            self):
        rel_fps = ['linear_regressions',
                   'linear_regressions_minimal']
        abs_fps = [self.get_data_path(rel_fp)
                     for rel_fp in rel_fps]

        input_objs = [self.LINREGOBJ_1_2_3,
            LinearRegressionsObjects(
                self.TEST_DICT_1,
                [])]

        for i in range(len(abs_fps)):
            abs_fp = abs_fps[i]
            input_obj = input_objs[i]
            out_format = linear_regressions_objects_to_linear_regressions_directory_format(input_obj)
            expected_format = \
                LinearRegressionsDirectoryFormat(abs_fp, mode='r')

            for exp_obs_pair in \
                    self.compare_linear_regressions_directory_formats(
                        expected_format, out_format):
                self.assertEqual(exp_obs_pair[0], exp_obs_pair[1])