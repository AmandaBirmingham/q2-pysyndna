import pandas
from pandas.testing import assert_frame_equal
from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase
from q2_types.feature_data import FeatureData

from pysyndna.tests.test_quant_orfs import TestQuantOrfsData
from q2_pysyndna import (
    __package_name__,
    CoordsFormat, CoordsDirectoryFormat,
    Coords)
from q2_pysyndna._type_format_coords import (
    coords_fp_to_df, df_to_coords_format)


class TestCoordsTypes(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_length_semantic_types_registration(self):
        self.assertRegisteredSemanticType(Coords)
        self.assertSemanticTypeRegisteredToFormat(
            FeatureData[Coords], CoordsDirectoryFormat)


class TestTSVLengthFormat(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_coords_format_valid(self):
        filenames = ['coords.txt']
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            test_format = CoordsFormat(filepath, mode='r')
            test_format.validate()

    def test_coords_format_invalid(self):
        expected_msg = "lengths.tsv is malformed or missing: list index " \
                       "out of range"
        filepath = self.get_data_path('feature_length/lengths.tsv')

        with self.assertRaisesRegex(ValidationError, expected_msg):
            test_format = CoordsFormat(filepath, mode='r')
            test_format.validate()


class TestCoordsTransformers(TestPluginBase):
    package = f'{__package_name__}.tests'

    TEST_DF = pandas.DataFrame(TestQuantOrfsData.COORDS_DICT)

    def test_coords_fp_to_df(self):
        test_fp = self.get_data_path('coords.txt')
        out_df = coords_fp_to_df(test_fp)
        assert_frame_equal(self.TEST_DF, out_df)

    def test_df_to_coords_format(self):
        input_df = pandas.DataFrame(TestQuantOrfsData.COORDS_DICT)
        expected_contents = ('G000005825_1\t816\t2168\n'
                             'G000005825_2\t2348\t3490\n'
                             'G000005825_3\t3744\t3959\n'
                             'G000005825_4\t3971\t5086\n'
                             'G000005825_5\t5098\t5373\n'
                             'G900163845_3247\t3392209\t3390413\n'
                             'G900163845_3248\t3393051\t3392206\n'
                             'G900163845_3249\t3393938\t3393048\n'
                             'G900163845_3250\t3394702\t3393935\n'
                             'G900163845_3251\t3395077\t3395721')

        # ensure the new format is filled with the expected contents
        test_format = df_to_coords_format(input_df)

        with test_format.open() as fh:
            out_contents = fh.read()
        self.assertEqual(expected_contents.strip(), out_contents.strip())

# NB: No tests for CoordsDirectoryFormat because it's a single-file one
