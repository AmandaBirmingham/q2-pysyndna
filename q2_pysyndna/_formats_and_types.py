from pysyndna.src.fit_syndna_models import SYNDNA_INDIV_NG_UL_KEY, \
    REGRESSION_KEYS
from qiime2.plugin import SemanticType
import qiime2.plugin.model as model
import yaml


# Types
SyndnaPools = SemanticType("SyndnaPools")
LinearRegressions = SemanticType("LinearRegressions")

# Formats
class SyndnaPoolsYamlFormat(model.TextFileFormat):
    """Represents a yaml file of concentrations of each syndna in each pool."""

    def _validate_(self, level):
        # Not a lot we can validate here as we don't know the name of the
        # syndna pool(s) or the names of the syndnas in them or the
        # concentrations of the syndnas in the pool(s), but we can at least
        # make sure that the file is legitimate yaml and that it contains
        # the expected top-level key with at least one child key that itself
        # has at least one child key, with a value that is a positive float.
        with self.path.open("r") as f:
            config_dict = yaml.safe_load(f)

        if not isinstance(config_dict, dict):
            raise ValueError("Expected a dictionary, but got %r" % config_dict)

        if SYNDNA_INDIV_NG_UL_KEY not in config_dict:
            raise ValueError("Expected a top-level key named %r, but got %r"
                             % (SYNDNA_INDIV_NG_UL_KEY, config_dict))

        if not isinstance(config_dict[SYNDNA_INDIV_NG_UL_KEY], dict):
            raise ValueError("Expected a dictionary of syndna pool(s) "
                             "as the value of the top-level key %r, but got %r"
                             % (SYNDNA_INDIV_NG_UL_KEY,
                                config_dict[SYNDNA_INDIV_NG_UL_KEY]))

        if len(config_dict[SYNDNA_INDIV_NG_UL_KEY]) == 0:
            raise ValueError("Expected a key for at least one syndna pool as "
                             "the value of the top-level key %r, but got none"
                             % SYNDNA_INDIV_NG_UL_KEY)

        for pool_name, pool_dict in config_dict[SYNDNA_INDIV_NG_UL_KEY].items():
            if not isinstance(pool_dict, dict):
                raise ValueError("Expected a dictionary of syndnas as the "
                                 "value of the key %r, but got %r"
                                 % (pool_name, pool_dict))

            if len(pool_dict) == 0:
                raise ValueError("Expected a key for at least one syndna in "
                                 "the pool %r, but got none" % pool_name)

            for syndna_name, conc in pool_dict.items():
                if not isinstance(conc, (int, float)):
                    raise ValueError("Expected a numeric concentration as "
                                     "the value of the syndna %r, "
                                     "but got %r" % (syndna_name, conc))

                if conc <= 0:
                    raise ValueError("Expected a positive concentration as "
                                     "the value of the syndna %r, but got %r"
                                     % (syndna_name, conc))


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

        if not isinstance(config_dict, dict):
            raise ValueError("Expected a dictionary, but got %r" % config_dict)

        if len(config_dict) == 0:
            raise ValueError("Expected at least one regression, but got none")

        for regression_name, regression_dict in config_dict.items():
            if regression_dict is not None:
                if not isinstance(regression_dict, dict):
                    raise ValueError(
                        "Expected None or a dictionary of regression "
                        "information as the value of the key %r, "
                        "but got %r" % (regression_name, regression_dict))

                # if there are any values in REGRESSION_KEYS that are not in
                # the keys of this regression dictionary, then raise an error
                missing_keys = set(REGRESSION_KEYS) - \
                    set(regression_dict.keys())
                if len(missing_keys) > 0:
                    raise ValueError(
                        f"Regression for {regression_name} does not "
                        f"include the following required keys: {missing_keys}")

                for required_key in REGRESSION_KEYS:
                    value = regression_dict[required_key]
                    if not isinstance(value, float):
                        raise ValueError("Expected a float as the value of "
                                         "the regression information key %r, "
                                         "but got %r" % (required_key, value))
