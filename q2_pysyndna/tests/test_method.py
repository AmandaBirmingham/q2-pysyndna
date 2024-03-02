import biom
import numpy as np
import pandas as pd
from qiime2 import Metadata
from qiime2.plugin.testing import TestPluginBase

from pysyndna.tests.test_fit_syndna_models import FitSyndnaModelsTestData, \
    SYNDNA_ID_KEY
from pysyndna.tests.test_calc_cell_counts import TestCalcCellCountsData, \
    SAMPLE_ID_KEY, GDNA_CONCENTRATION_NG_UL_KEY, ELUTE_VOL_UL_KEY, \
    SEQUENCED_SAMPLE_GDNA_MASS_NG_KEY, SAMPLE_TOTAL_READS_KEY, \
    OGU_ID_KEY, OGU_CELLS_PER_G_OF_GDNA_KEY, SAMPLE_IN_ALIQUOT_MASS_G_KEY
from pysyndna.tests.test_quant_orfs import TestQuantOrfsData, OGU_ORF_ID_KEY
from pysyndna.tests.test_util import Testers
from q2_pysyndna import __package_name__, fit, count_cells, count_copies
from q2_pysyndna._type_format_linear_regressions import \
    LinearRegressionsObjects


class TestFit(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_fit(self):
        min_count = 50

        syndna_concs_df = pd.DataFrame(FitSyndnaModelsTestData.syndna_concs_dict)
        sample_syndna_weights_and_total_reads_df = pd.DataFrame(
            FitSyndnaModelsTestData.a_b_sample_syndna_weights_and_total_reads_dict)
        sample_syndna_weights_and_total_reads_df.set_index(
            SAMPLE_ID_KEY, inplace=True)
        metadata = Metadata(sample_syndna_weights_and_total_reads_df)

        reads_per_syndna_per_sample_df = pd.DataFrame(
            FitSyndnaModelsTestData.reads_per_syndna_per_sample_dict)
        reads_per_syndna_per_sample_df.set_index(SYNDNA_ID_KEY, inplace=True)

        input_biom = biom.table.Table(
            FitSyndnaModelsTestData.reads_per_syndna_per_sample_array,
            FitSyndnaModelsTestData.reads_per_syndna_per_sample_dict[SYNDNA_ID_KEY],
            FitSyndnaModelsTestData.sample_ids)

        out_linregress_dict, out_msgs = fit(
            syndna_concs_df,
            input_biom,
            metadata, min_count)

        a_tester = Testers()
        a_tester.assert_dicts_almost_equal(
            FitSyndnaModelsTestData.lingress_results, out_linregress_dict)
        self.assertEqual([], out_msgs)


class TestCountCells(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_count_cells(self):
        params_dict = {k: TestCalcCellCountsData.sample_and_prep_input_dict[k]
                       for k in
                       [SAMPLE_ID_KEY, SAMPLE_IN_ALIQUOT_MASS_G_KEY,
                        GDNA_CONCENTRATION_NG_UL_KEY, ELUTE_VOL_UL_KEY,
                        SEQUENCED_SAMPLE_GDNA_MASS_NG_KEY]}
        params_dict[SAMPLE_TOTAL_READS_KEY] = \
            TestCalcCellCountsData.mass_and_totals_dict[SAMPLE_TOTAL_READS_KEY]

        counts_vals = TestCalcCellCountsData.make_combined_counts_np_array()

        params_df = pd.DataFrame(params_dict)
        params_df.set_index(SAMPLE_ID_KEY, inplace=True)
        metadata = Metadata(params_df)

        counts_biom = biom.table.Table(
            counts_vals,
            TestCalcCellCountsData.ogu_lengths_dict[OGU_ID_KEY],
            params_dict[SAMPLE_ID_KEY])
        lengths_df = pd.DataFrame(TestCalcCellCountsData.ogu_lengths_dict)
        # Note that, in the output, the ogu_ids are apparently sorted
        # alphabetically--different than the input order
        expected_out_biom = biom.table.Table(
            np.array(TestCalcCellCountsData.reordered_results_dict[
                         OGU_CELLS_PER_G_OF_GDNA_KEY]),
            TestCalcCellCountsData.reordered_results_dict[OGU_ID_KEY],
            TestCalcCellCountsData.reordered_results_dict[SAMPLE_ID_KEY])

        read_len = 150
        min_coverage = 1
        min_rsquared = 0.8
        output_metric = OGU_CELLS_PER_G_OF_GDNA_KEY

        linregs_objs = LinearRegressionsObjects(
            TestCalcCellCountsData.linregresses_dict, ["test fit msg"])

        # Note: 1) this is outputting the ogu_cell_counts_per_g_gdna, not the
        # ogu_cell_counts_per_g_sample (which is what is output by the qiita
        # version of this function) because I want to check that I really can
        # choose to get something else, and 2) this is using the full version
        # of Avogadro's #, not the truncated version that was used in the
        # notebook, so the results are slightly different (but more realistic)
        output_biom, output_msgs = count_cells(
            linregs_objs, counts_biom, lengths_df, metadata,
            read_len, min_coverage, min_rsquared, output_metric)

        # NB: only checking results to 2 decimals because Ubuntu and Mac
        # differ past that point. Not that it matters much since the decimal
        # portion of values this huge is not very important.
        a_tester = Testers()
        a_tester.assert_biom_tables_equal(expected_out_biom, output_biom,
                                          decimal_precision=2)
        self.assertListEqual(
            ["The following items have % coverage lower than the minimum of "
             "1.0: ['example2;Neisseria subflava', "
             "'example2;Haemophilus influenzae']"],
            output_msgs)


class TestCountCopies(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_count_copies(self):
        input_quant_params_per_sample_df = pd.DataFrame(
            TestQuantOrfsData.PARAMS_DICT)
        input_quant_params_per_sample_df.set_index(SAMPLE_ID_KEY, inplace=True)
        metadata = Metadata(input_quant_params_per_sample_df)

        ogu_orf_coords_df = pd.DataFrame(TestQuantOrfsData.COORDS_DICT)

        input_reads_per_ogu_orf_per_sample_biom = biom.table.Table(
            TestQuantOrfsData.COUNT_VALS,
            TestQuantOrfsData.LEN_AND_COPIES_DICT[OGU_ORF_ID_KEY],
            TestQuantOrfsData.SAMPLE_IDS)

        expected_biom = biom.table.Table(
            TestQuantOrfsData.COPIES_PER_G_SAMPLE_VALS,
            TestQuantOrfsData.LEN_AND_COPIES_DICT[OGU_ORF_ID_KEY],
            TestQuantOrfsData.SAMPLE_IDS)

        output_biom, output_msgs = count_copies(
            input_reads_per_ogu_orf_per_sample_biom,
            ogu_orf_coords_df, metadata)

        # NB: Comparing the bioms as dataframes because the biom equality
        # compare does not allow "almost equal" checking for float values,
        # whereas rtol and atol are built in to assert_frame_equal
        output_df = output_biom.to_dataframe()
        expected_df = expected_biom.to_dataframe()
        pd.testing.assert_frame_equal(output_df, expected_df)

        self.assertListEqual([], output_msgs)
