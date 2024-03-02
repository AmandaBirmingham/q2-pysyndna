import pandas
from pandas.testing import assert_frame_equal
from qiime2.plugin.testing import TestPluginBase
from q2_pysyndna import (
    __package_name__, SyndnaPoolCsvFormat, LinearRegressionsYamlFormat,
    PysyndnaLogFormat)


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

