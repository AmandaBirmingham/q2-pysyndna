import pandas
from qiime2.plugin import SemanticType, ValidationError
import qiime2.plugin.model as model

from pysyndna.src.fit_syndna_models import \
   SYNDNA_ID_KEY, SYNDNA_INDIV_NG_UL_KEY

# Types
SyndnaPoolConcentrationTable = SemanticType("SyndnaPoolConcentrationTable")


# Formats
class SyndnaPoolCsvFormat(model.TextFileFormat):
    """Represents a csv file of concentrations of each syndna in one pool."""

    def _validate_(self, level):
        # Validate that the file is a csv and that it has the expected columns.
        # Note that we don't validate the values in the columns, as we don't
        # know what they should be.
        with self.path.open("r") as f:
            df = pandas.read_csv(f, header=0, comment="#")

        if (len(df.columns) != 2) or (df.columns[0] != SYNDNA_ID_KEY) or \
                (df.columns[1] != SYNDNA_INDIV_NG_UL_KEY):
            raise ValidationError(
                f"Expected exactly two columns '{SYNDNA_ID_KEY}' and "
                f"'{SYNDNA_INDIV_NG_UL_KEY}', but got {df.columns}")

        if len(df) == 0:
            raise ValidationError("Expected at least one row, but got none")


# So ...
# https://dev.qiime2.org/latest/storing-data/formats/#single-file-directory-formats
# states:
# "Currently QIIME 2 requires that all formats registered to a Semantic Type
# be a directory format .... For [single file format] cases, there exists a
# factory for quickly constructing directory layouts that contain only a
# single file. This requirement might be removed in the future, but for now it
# is a necessary evil (and also isn’t too much extra work for format
# developers)."
# Ok then, here goes:
SyndnaPoolDirectoryFormat = model.SingleFileDirectoryFormat(
    'SyndnaPoolDirectoryFormat',
    'syndna_pool.csv', SyndnaPoolCsvFormat)


def syndna_pool_csv_format_to_df(ff: SyndnaPoolCsvFormat) -> pandas.DataFrame:
    result = pandas.read_csv(str(ff), header=0, comment='#')
    return result
