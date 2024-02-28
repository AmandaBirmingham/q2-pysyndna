from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_pysyndna import (
    __package_name__,
    PysyndnaLogFormat, PysyndnaLogDirectoryFormat,
    PysyndnaLog)
from q2_pysyndna._type_format_pysyndna_log import (
    extract_fp_from_directory_format,
    load_list_from_pysyndnalog_fp, fill_pysyndnalogformat,
    extract_list_from_pysyndnalogdir_format)


class TestPysyndnaLogTypes(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_pysyndna_log_semantic_types_registration(self):
        self.assertRegisteredSemanticType(PysyndnaLog)
        self.assertSemanticTypeRegisteredToFormat(
            PysyndnaLog,
            PysyndnaLogDirectoryFormat)


class TestPysyndnaLogFormat(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_pysyndnalog_format_valid(self):
        filenames = ['linear_regressions/linear_regressions.log',
                     'linear_regressions_minimal/linear_regressions.log']
        filepaths = [self.get_data_path(filename)
                     for filename in filenames]

        for filepath in filepaths:
            test_format = PysyndnaLogFormat(filepath, mode='r')
            test_format.validate()

    def test_pysyndnalog_format_invalid(self):
        made_up_path = self.get_data_path('made_up_filename')
        with self.assertRaisesRegex(ValidationError, r'is not a file.'):
            test_format = PysyndnaLogFormat(made_up_path, mode='r')
            test_format.validate()


class TestPysyndnaLogHelpers(TestPluginBase):
    package = f'{__package_name__}.tests'

    def test_extract_fp_from_directory_format(self):
        # create a directory format with a file format in it
        test_file_format = PysyndnaLogFormat()
        with test_file_format.open() as fh:
            fh.write("test content")
        test_dir_format = PysyndnaLogDirectoryFormat()
        test_dir_format.file.write_data(test_file_format, PysyndnaLogFormat)

        # ensure can pull the filepath of the file format out of it; since
        # PysyndnaDirectoryFormat is a single-file directory format, it will
        # always have a "file" property
        out_fp = extract_fp_from_directory_format(
            test_dir_format, test_dir_format.file)

        # there's not a good way to test that we got the right filepath, since
        # the file is stored in a temporary directory, so just test that we got
        # a string that ends with what we expect
        self.assertTrue(out_fp.endswith('/pysyndna.log'))

    def test_load_pysyndnalog_fp(self):
        expected_list = ["The following syndnas were dropped because they "
                         "had fewer than 200 total reads aligned:['p166']"]

        test_fp = self.get_data_path(
            'linear_regressions/linear_regressions.log')
        out_list = load_list_from_pysyndnalog_fp(test_fp)
        self.assertEqual(expected_list, out_list)

    def test_fill_pysyndnalogformat_wo_format_input(self):
        test_logs = ["log msg 1", "log msg 2"]
        expected_contents = 'log msg 1\nlog msg 2'

        # ensure the new format is filled with the expected contents
        test_format = fill_pysyndnalogformat(test_logs)

        with test_format.open() as fh:
            self.assertEqual(fh.read(), expected_contents)

    def test_fill_pysyndnalogformat_w_format_input(self):
        test_format = PysyndnaLogFormat()
        test_logs = ["log msg 1", "log msg 2"]
        expected_contents = 'log msg 1\nlog msg 2'

        # ensure the existing format is filled with the expected contents
        _ = fill_pysyndnalogformat(test_logs, test_format)

        with test_format.open() as fh:
            self.assertEqual(fh.read(), expected_contents)

    def test_extract_list_from_pysyndnalogdir_format(self):
        expected_content = "test content"

        # create a directory format with a file format in it
        test_file_format = PysyndnaLogFormat()
        with test_file_format.open() as fh:
            fh.write(expected_content)
        test_dir_format = PysyndnaLogDirectoryFormat()
        test_dir_format.file.write_data(test_file_format, PysyndnaLogFormat)

        # ensure the expected content is extracted from the directory format
        out_list = extract_list_from_pysyndnalogdir_format(test_dir_format)
        self.assertEqual(out_list, [expected_content])

# NB: No tests for PysyndnaLogDirectoryFormat because it's a single-file one
