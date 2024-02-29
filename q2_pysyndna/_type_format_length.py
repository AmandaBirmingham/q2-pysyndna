import pandas
from qiime2.plugin import SemanticType, ValidationError
import qiime2.plugin.model as model
from q2_types.feature_data import FeatureData

FEATURE_NAME_KEY = 'Feature ID'
LENGTH_KEY = 'length'
OBSERVATION_KEY = 'observation'

Length = SemanticType('Length', variant_of=FeatureData.field['type'])


class TSVLengthFormat(model.TextFileFormat):
    """Format for a 2 column TSV file without a header.

    There must be at least one line of data and second column must be integers.
    """

    def _validate_(self, level):
        _ = tsvlength_fp_to_dataframe(str(self.path))


TSVLengthDirectoryFormat = model.SingleFileDirectoryFormat(
    'TSVLengthDirectoryFormat', 'lengths.tsv', TSVLengthFormat)


def tsvlength_fp_to_dataframe(fp: str) -> pandas.DataFrame:
    # Using `dtype=object` and `set_index()` to avoid type casting/inference of
    # any columns or the index.
    df = pandas.read_csv(fp, sep='\t', header=None, index_col=0,
                         skip_blank_lines=True, dtype=object)

    df.index.name = FEATURE_NAME_KEY
    df.columns = [LENGTH_KEY]

    checked_df = _validate_and_cast_tsvlength_df(df)
    return checked_df


def dataframe_to_tsvlength_format(df):
    df = _validate_and_cast_tsvlength_df(df)
    ff = TSVLengthFormat()
    df.to_csv(str(ff), sep='\t', header=False, index=True)
    return ff


def _validate_and_cast_tsvlength_df(df: pandas.DataFrame) -> pandas.DataFrame:
    if len(df.index) < 1:
        raise ValidationError("Length format requires at least one row of data.")

    if len(df.columns) != 1:
        raise ValidationError(
            "Length format requires at one column of data.")

    if df.index.name != FEATURE_NAME_KEY:
        raise ValidationError(
            f"Length format requires the dataframe index name to be "
            f"`{FEATURE_NAME_KEY}`, found {df.index.name}")

    if df.columns[0] != LENGTH_KEY:
        raise ValidationError(
            f"Length format requires the first column name to be"
            f" `{LENGTH_KEY}`, found {df.columns[0]}")

    if df.index.has_duplicates:
        raise ValidationError(
            "Length format feature IDs must be unique. The following IDs "
            "are duplicated: %s" %
            ', '.join(df.index[df.index.duplicated()].unique()))

    # convert the length column to integers
    try:
        df[LENGTH_KEY] = df[LENGTH_KEY].astype(int)
    except ValueError:
        raise ValidationError(
            "Lengths must be integers, but found non-integer values.")
    # error if any of the lengths are negative or nan
    if (df[LENGTH_KEY] < 0).any() or df[LENGTH_KEY].isna().any():
        raise ValidationError("Lengths must be non-negative integers.")

    return df
