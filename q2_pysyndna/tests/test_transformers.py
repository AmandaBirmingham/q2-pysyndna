import pandas
from pandas.testing import assert_frame_equal
from qiime2.plugin.testing import TestPluginBase
from q2_pysyndna import (
    __package_name__, SyndnaPoolCsvFormat, LinearRegressionsYamlFormat,
    LinearRegressionsLogFormat)
import q2_pysyndna.plugin_setup as plugin_setup


class TestSyndnaPoolCsvFormatTransformers(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_syndna_pool_csv_format_to_dataframe(self):
        input_fname = "syndna_pool.csv"

        expected_dict = {
            "syndna_id": ["p126", "p136", "p146", "p156", "p166",
                          "p226", "p236", "p246", "p256", "p266"],
            "syndna_indiv_ng_ul": [1, 0.1, 0.01, 0.001, 0.0001,
                                   0.0001, 0.001, 0.01, 0.1, 1]
        }

        expected_df = pandas.DataFrame(expected_dict)

        _, obs_df = self.transform_format(
            SyndnaPoolCsvFormat, pandas.DataFrame,
            filename=input_fname)

        assert_frame_equal(obs_df, expected_df)


class TestLinearRegressionsYamlFormatTransformers(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_dict_linear_regression_yaml_format(self):
        # TODO: fill in functionality
        pass

        # input_dict = {"example1": {
        #         "slope": 1.24487652379132,
        #         "intercept": -6.77539505390338,
        #         "rvalue": 0.9865030975156575,
        #         "pvalue": 1.428443560659758e-07,
        #         "stderr": 0.07305408550335003,
        #         "intercept_stderr": 0.2361976278251443},
        #     "example2": {
        #         "slope": 1.24675913604407,
        #         "intercept": -7.155318973708384,
        #         "rvalue": 0.9863241797356326,
        #         "pvalue": 1.505381146809759e-07,
        #         "stderr": 0.07365795255302438,
        #         "intercept_stderr": 0.2563956755844754},
        #     "example3": None}
        #
        # expected_content_fp = self.get_data_path(
        #     "data/linear_regressions.yaml")
        # test_format = SyndnaPoolCsvFormat(input_fp, mode='r')
        # output_df = plugin_setup._1(test_format)
        #
        # assert_frame_equal(output_df, expected_df)
