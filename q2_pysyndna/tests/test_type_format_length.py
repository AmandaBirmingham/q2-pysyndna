import pandas
from pandas.testing import assert_frame_equal
from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase
from q2_types.feature_data import FeatureData

from q2_pysyndna import (
    __package_name__,
    TSVLengthFormat, TSVLengthDirectoryFormat,
    Length)
from q2_pysyndna._type_format_length import (
    tsvlength_fp_to_dataframe,
    dataframe_to_tsvlength_format, biom_to_tsvlength_format,
    FEATURE_NAME_KEY, LENGTH_KEY)


class TestLengthTypes(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_length_semantic_types_registration(self):
        self.assertRegisteredSemanticType(Length)
        self.assertSemanticTypeRegisteredToFormat(
            FeatureData[Length], TSVLengthDirectoryFormat)


class TestTSVLengthFormat(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_tsvlength_format_valid(self):
        filenames = ['feature_length/lengths.tsv']
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            test_format = TSVLengthFormat(filepath, mode='r')
            test_format.validate()

    def test_tsvlength_format_duplicate_invalid(self):
        expected_msg = "Length format feature IDs must be unique. The " \
                       "following IDs are duplicated: G000005825"
        filepath = self.get_data_path('feature_lengths_malformed_1.tsv')

        with self.assertRaisesRegex(ValidationError, expected_msg):
            test_format = TSVLengthFormat(filepath, mode='r')
            test_format.validate()

    def test_tsvlength_format_notint_invalid(self):
        expected_msg = \
            "Lengths must be integers, but found non-integer values."
        filepath = self.get_data_path('feature_lengths_malformed_2.tsv')

        with self.assertRaisesRegex(ValidationError, expected_msg):
            test_format = TSVLengthFormat(filepath, mode='r')
            test_format.validate()

    def test_tsvlength_format_negint_invalid(self):
        expected_msg = "Lengths must be non-negative integers."
        filepath = self.get_data_path('feature_lengths_malformed_3.tsv')

        with self.assertRaisesRegex(ValidationError, expected_msg):
            test_format = TSVLengthFormat(filepath, mode='r')
            test_format.validate()


class TestTSVLengthHelpers(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_tsvlength_fp_to_dataframe(self):
        expected_df = pandas.DataFrame(
            index=["G000005825", "G000006175", "G000006605", "G000006725",
                   "G000006745", "G000006785", "G000006845", "G000006865",
                   "G000006925", "G000006965", "G000006985", "G000007005"],
            data={LENGTH_KEY: [
                4249288, 1936387, 2476842, 2731790, 4033484, 1852433,
                2153922, 2365589, 4828840, 6691734, 2154946, 2992245]})
        expected_df.index.name = FEATURE_NAME_KEY
        test_fp = self.get_data_path('feature_length/lengths.tsv')
        out_df = tsvlength_fp_to_dataframe(test_fp)
        assert_frame_equal(expected_df, out_df)

    def test_dataframe_to_tsvlength_format(self):
        input_df = pandas.DataFrame(
            index=["G000005825", "G000006175", "G000006605", "G000006725",
                   "G000006745", "G000006785", "G000006845", "G000006865",
                   "G000006925", "G000006965", "G000006985", "G000007005"],
            data={LENGTH_KEY: [
                4249288, 1936387, 2476842, 2731790, 4033484, 1852433,
                2153922, 2365589, 4828840, 6691734, 2154946, 2992245]})
        input_df.index.name = FEATURE_NAME_KEY

        # ensure the new format is filled with the expected contents
        test_format = dataframe_to_tsvlength_format(input_df)

        expected_contents_fp = self.get_data_path(
            'feature_length/lengths.tsv')
        with open(expected_contents_fp, 'r') as fc:
            expected_contents = fc.read()

        with test_format.open() as fh:
            out_contents = fh.read()

        self.assertEqual(expected_contents.strip(), out_contents.strip())

    def test_dataframe_to_tsvlength_format_fail(self):
        input_df = pandas.DataFrame(
            index=["G000005825", "G000006175", "G000006605", "G000006725",
                   "G000006745", "G000006785", "G000006845", "G000006865",
                   "G000006925", "G000006965", "G000006985", "G000007005"],
            data={LENGTH_KEY: [
                -4249288, 1936387, 2476842, 2731790, 4033484, 1852433,
                2153922, 2365589, 4828840, 6691734, 2154946, 2992245]})
        input_df.index.name = FEATURE_NAME_KEY

        with self.assertRaisesRegex(
                ValidationError, "Lengths must be non-negative integers."):
            dataframe_to_tsvlength_format(input_df)

# NB: No tests for TSVLengthDirectoryFormat because it's a single-file one
