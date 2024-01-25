import pandas
#from pysyndna.src.fit_syndna_models import \
#    SYNDNA_ID_KEY, SYNDNA_INDIV_NG_UL_KEY, REGRESSION_KEYS
from qiime2.plugin import SemanticType, ValidationError
import qiime2.plugin.model as model
import yaml

# TODO: remove local string literal definitions after debugging complete
SYNDNA_ID_KEY = "syndna_id"
SYNDNA_INDIV_NG_UL_KEY = "syndna_indiv_ng_ul"
REGRESSION_KEYS = ["slope", "intercept", "rvalue", "pvalue", "stderr",
                   "intercept_stderr"]


# Types
SyndnaPoolConcentrationTable = SemanticType("SyndnaPoolConcentrationTable")
LinearRegressions = SemanticType("LinearRegressions")


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


class LinearRegressionsYamlFormat(model.TextFileFormat):
    """Represents a yaml file of linear regression models."""

    def _validate_(self, level):
        # Not a lot we can validate here as we don't know the names of the
        # regressions or how many there will be, but we can at least make sure
        # that the file is legitimate yaml and that every top-level key has
        # a value that is None or is a dictionary that contains at least the
        # required keys, all of which are floats.
        with self.path.open("r") as f:
            config_dict = yaml.safe_load(f)

        if config_dict is None:
            raise ValidationError(
                "Expected at least one regression, but got none")

        if not isinstance(config_dict, dict):
            raise ValidationError(
                "Expected a dictionary, but got %r" % config_dict)

        for regression_name, regression_dict in config_dict.items():
            if regression_dict is not None:
                if not isinstance(regression_dict, dict):
                    raise ValidationError(
                        "Expected None or a dictionary of regression "
                        "information as the value of the key %r, "
                        "but got %r" % (regression_name, regression_dict))

                # if there are any values in REGRESSION_KEYS that are not in
                # the keys of this regression dictionary, then raise an error
                missing_keys = set(REGRESSION_KEYS) - \
                    set(regression_dict.keys())
                if len(missing_keys) > 0:
                    raise ValidationError(
                        f"Expected regression for {regression_name} to "
                        f"include the following required keys: {missing_keys}")

                for required_key in REGRESSION_KEYS:
                    value = regression_dict[required_key]
                    if not isinstance(value, float):
                        raise ValidationError(
                            "Expected a float as the value of the regression "
                            "information key %r, but got %r" %
                            (required_key, value))


class LinearRegressionsLogFormat(model.TextFileFormat):
    """Represents a log file of messages about linear regression modeling."""

    def _validate_(self, level):
        # Validate that it's a readable text file ... no contents required.
        with self.path.open("r") as f:
            pass


class LinearRegressionsDirectoryFormat(model.DirectoryFormat):
    """Represents a yaml file of linear regression models and a log."""

    linregs_yaml = model.File(
        r'linear_regressions.yaml', format=LinearRegressionsYamlFormat)
    log = model.File(
        r'linear_regressions.log', format=LinearRegressionsLogFormat)
