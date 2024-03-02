import collections
from typing import Dict, Union, Optional
from qiime2.plugin import SemanticType, ValidationError
import qiime2.plugin.model as model
import yaml

from pysyndna.src.fit_syndna_models import REGRESSION_KEYS
from q2_pysyndna._type_format_pysyndna_log import PysyndnaLogFormat, \
    log_fp_to_list, extract_fp_from_directory_format, \
    list_to_pysyndna_log_format

LinearRegressionsObjects = collections.namedtuple(
    "LinearRegressionsObjects",
    ["linregs_dict", "log_msgs_list"])

LinearRegressions = SemanticType("LinearRegressions")


class LinearRegressionsYamlFormat(model.TextFileFormat):
    """Represents a yaml file of linear regression models."""

    def _validate_(self, level):
        _ = yaml_fp_to_linear_regressions_yaml_format(self.path)


class LinearRegressionsDirectoryFormat(model.DirectoryFormat):
    """Represents a yaml file of linear regression models and a log."""

    linregs_yaml = model.File(
        r'linear_regressions.yaml', format=LinearRegressionsYamlFormat)
    log = model.File(
        r'linear_regressions.log', format=PysyndnaLogFormat)


def yaml_fp_to_linear_regressions_yaml_format(yaml_fp) -> \
        Dict[str, Union[Dict[str, float], None]]:

    # Not a lot we can validate here as we don't know the names of the
    # regressions or how many there will be, but we can at least make sure
    # that the file is legitimate yaml and that every top-level key has
    # a value that is None or is a dictionary that contains at least the
    # required keys, all of which are floats.
    with open(yaml_fp, "r") as f:
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

    return config_dict


def dict_to_linear_regressions_yaml_format(
        data: Dict[str, Union[Dict[str, float], None]],
        ff: Optional[LinearRegressionsYamlFormat] = None) -> \
        LinearRegressionsYamlFormat:
    if ff is None:
        ff = LinearRegressionsYamlFormat()
    with ff.open() as fh:
        yaml.safe_dump(data, fh)
    return ff


def linear_regressions_directory_format_to_linear_regressions_objects(
        data: LinearRegressionsDirectoryFormat) -> LinearRegressionsObjects:
    linregs_fp = extract_fp_from_directory_format(data, data.linregs_yaml)
    linregs_dict = yaml_fp_to_linear_regressions_yaml_format(linregs_fp)

    log_fp = extract_fp_from_directory_format(data, data.log)
    log_msgs_list = log_fp_to_list(log_fp)

    result = LinearRegressionsObjects(linregs_dict, log_msgs_list)
    return result


def linear_regressions_objects_to_linear_regressions_directory_format(
        data: LinearRegressionsObjects) -> LinearRegressionsDirectoryFormat:
    fy = dict_to_linear_regressions_yaml_format(data.linregs_dict)
    fl = list_to_pysyndna_log_format(data.log_msgs_list)

    ff = LinearRegressionsDirectoryFormat()
    ff.linregs_yaml.write_data(fy, LinearRegressionsYamlFormat)
    ff.log.write_data(fl, PysyndnaLogFormat)
    return ff
