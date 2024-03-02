import os
import tempfile
import glob
from qiime2.plugin.testing import TestPluginBase

from q2_pysyndna import __package_name__, view_fit, view_log, \
    LinearRegressionsDirectoryFormat, PysyndnaLogDirectoryFormat
from q2_pysyndna._visualizer import INDEX_FNAME, FITS_FNAME, LOG_FNAME


class TestVisualizers(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_view_fit(self):
        expected_filelist = [FITS_FNAME, INDEX_FNAME, LOG_FNAME]
        abs_fp = self.get_data_path('linear_regressions')
        test_format = LinearRegressionsDirectoryFormat(abs_fp, mode='r')

        with tempfile.TemporaryDirectory() as output_dir:
            view_fit(output_dir, test_format)

            pattern = output_dir + '/*.html'
            filelist = [os.path.basename(x) for x in glob.glob(pattern)]
            filelist.sort()
            self.assertListEqual(expected_filelist, filelist)

            index_fp = os.path.join(output_dir, INDEX_FNAME)
            self.assertTrue('Fits' in open(index_fp).read())
            self.assertTrue('Log' in open(index_fp).read())

            fits_fp = os.path.join(output_dir, FITS_FNAME)
            self.assertTrue('slope: 1.24487652379132' in open(fits_fp).read())

            log_fp = os.path.join(output_dir, LOG_FNAME)
            self.assertTrue('fewer than 200 total' in open(log_fp).read())

    def test_view_log(self):
        expected_filelist = [INDEX_FNAME, LOG_FNAME]
        abs_fp = self.get_data_path('pysyndna_log')
        test_format = PysyndnaLogDirectoryFormat(abs_fp, mode='r')

        with tempfile.TemporaryDirectory() as output_dir:
            view_log(output_dir, test_format)

            pattern = output_dir + '/*.html'
            filelist = [os.path.basename(x) for x in glob.glob(pattern)]
            filelist.sort()
            self.assertListEqual(expected_filelist, filelist)

            index_fp = os.path.join(output_dir, INDEX_FNAME)
            self.assertTrue('Log' in open(index_fp).read())

            log_fp = os.path.join(output_dir, LOG_FNAME)
            self.assertTrue('fewer than 200 total' in open(log_fp).read())
