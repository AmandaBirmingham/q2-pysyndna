import pandas
from qiime2.plugin import SemanticType, ValidationError
import qiime2.plugin.model as model
from q2_types.feature_data import FeatureData

from pysyndna import read_ogu_orf_coords_to_df, \
    validate_and_cast_ogu_orf_coords_df

Coords = SemanticType('Coords', variant_of=FeatureData.field['type'])


# The text file format is rather specialized so its parsing and validation is
# punted to the pysyndna library, which really knows and cares :)
class CoordsFormat(model.TextFileFormat):
    """Text coords format used by woltka

    Format is shown below:
        >G000005825
        1	816	2168
        2	2348	3490
        3	3744	3959
        4	3971	5086
        5	5098	5373
        6	5432	7372
        7	7399	9966
        <etc.>.
    """

    def _validate_(self, level):
        _ = coords_fp_to_df(str(self.path))


CoordsDirectoryFormat = model.SingleFileDirectoryFormat(
    'CoordsDirectoryFormat', 'coords.txt', CoordsFormat)


def coords_fp_to_df(fp: str) -> pandas.DataFrame:
    try:
        df = read_ogu_orf_coords_to_df(fp)
    except Exception as e:
        raise ValidationError(f"File {fp} is malformed or missing: {e}")
    checked_df = validate_and_cast_ogu_orf_coords_df(df)
    return checked_df


def df_to_coords_format(df):
    df = validate_and_cast_ogu_orf_coords_df(df)
    ff = CoordsFormat()
    df.to_csv(str(ff), sep='\t', header=False, index=False)
    return ff
