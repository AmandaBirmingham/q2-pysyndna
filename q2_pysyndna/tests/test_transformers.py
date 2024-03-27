import pandas
from pandas.testing import assert_frame_equal
from qiime2.plugin.testing import TestPluginBase
from q2_pysyndna import (
    __package_name__, SyndnaPoolCsvFormat, LinearRegressionsYamlFormat,
    LinearRegressionsDirectoryFormat,
    PysyndnaLogFormat, PysyndnaLogDirectoryFormat,
    TSVLengthFormat, CoordsFormat)
from q2_pysyndna._type_format_linear_regressions import \
    LinearRegressionsObjects
from q2_pysyndna.tests.test_type_format_linear_regressions import \
    TestLinearRegressionsTransformers
from q2_pysyndna.tests.test_type_format_length import \
    TestTSVLengthTransformers
from q2_pysyndna.tests.test_type_format_coords import TestCoordsTransformers


class TestTransformers(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_syndna_pool_csv_format_to_df(self):
        expected_dict = {
            "syndna_id": ["p126", "p136", "p146", "p156", "p166",
                          "p226", "p236", "p246", "p256", "p266"],
            "syndna_indiv_ng_ul": [1, 0.1, 0.01, 0.001, 0.0001,
                                   0.0001, 0.001, 0.01, 0.1, 1]
        }

        expected_df = pandas.DataFrame(expected_dict)

        _, obs_df = self.transform_format(
            SyndnaPoolCsvFormat, pandas.DataFrame,
            filename="syndna_pool.csv")

        assert_frame_equal(obs_df, expected_df)

    def test_pysyndna_log_format_to_list(self):
        expected_list = ["The following syndnas were dropped because they "
                         "had fewer than 200 total reads aligned:['p166']"]

        _, obs_df = self.transform_format(
            PysyndnaLogFormat, list,
            filename="linear_regressions/linear_regressions.log")

        self.assertListEqual(expected_list, obs_df)

    def test_pysyndna_log_directory_format_to_list(self):
        expected_list = ["The following syndnas were dropped because they "
                         "had fewer than 200 total reads aligned:['p166']"]

        _, obs_list = self.transform_format(
            PysyndnaLogDirectoryFormat, list,
            filename="pysyndna_log")

        self.assertListEqual(expected_list, obs_list)

    def test_linear_regressions_yaml_format_to_dict(self):
        _, obs_dict = self.transform_format(
            LinearRegressionsYamlFormat, dict,
            filename="linear_regressions/linear_regressions.yaml")

        self.assertDictEqual(
            TestLinearRegressionsTransformers.TEST_DICT_1_2_3, obs_dict)

    def test_linear_regressions_directory_format_to_linear_regressions_objects(
            self):
        _, obs_objs = self.transform_format(
            LinearRegressionsDirectoryFormat,
            LinearRegressionsObjects,
            filename="linear_regressions")

        self.assertTupleEqual(
            TestLinearRegressionsTransformers.LINREGOBJ_1_2_3, obs_objs)

    def test_linear_regressions_objects_to_linear_regressions_directory_format(
            self):

        format_fp = self.get_data_path("linear_regressions")
        expected_format = LinearRegressionsDirectoryFormat(format_fp, mode="r")

        transformer = self.get_transformer(
            LinearRegressionsObjects, LinearRegressionsDirectoryFormat)
        obs_format = transformer(
            TestLinearRegressionsTransformers.LINREGOBJ_1_2_3)

        for exp_obs_pair in \
            TestLinearRegressionsTransformers.compare_linear_regressions_directory_formats(
                expected_format, obs_format):
            self.assertEqual(exp_obs_pair[0], exp_obs_pair[1])

    def test_tsv_length_format_to_df(self):
        _, obs_df = self.transform_format(
            TSVLengthFormat,
            pandas.DataFrame,
            filename="feature_length/lengths.tsv")

        assert_frame_equal(obs_df, TestTSVLengthTransformers.TEST_DF)

    def test_coords_format_to_df(self):
        _, obs_df = self.transform_format(
            CoordsFormat,
            pandas.DataFrame,
            filename="coords.txt")

        assert_frame_equal(obs_df, TestCoordsTransformers.TEST_DF)
