import importlib_resources
import os
import q2templates
import yaml

from q2_pysyndna._settings import __package_name__
from q2_pysyndna._type_format_pysyndna_log import PysyndnaLogDirectoryFormat, \
    pysyndna_log_directory_format_to_list
from q2_pysyndna._type_format_linear_regressions import \
    LinearRegressionsDirectoryFormat, \
    linear_regressions_directory_format_to_linear_regressions_objects

LOG_FNAME = 'log.html'
FITS_FNAME = 'fits.html'
INDEX_FNAME = 'index.html'
TABS_KEY = 'tabs'
URL_KEY = 'url'
TITLE_KEY = 'title'

REF = importlib_resources.files(__package_name__) / 'assets'
# replaces pkg_resources.resource_filename() idiom from older plugins,
# since pkg_resources API is now deprecated.
# NB: below method is not robust to files inside zips; see
# https://importlib-resources.readthedocs.io/en/latest/migration.html#pkg-resources-resource-filename
with importlib_resources.as_file(REF) as path:
    TEMPLATES = str(path)


def view_fit(output_dir: str,
             linear_regressions: LinearRegressionsDirectoryFormat) -> None:
    html_fnames = []
    context = _check_context({})

    linear_reg_objs = \
        linear_regressions_directory_format_to_linear_regressions_objects(
            linear_regressions)

    linregs_yaml_str = yaml.dump(linear_reg_objs.linregs_dict)
    context['linregs_yaml'] = linregs_yaml_str
    context[TABS_KEY].append({URL_KEY: FITS_FNAME, TITLE_KEY: 'Fits'})
    html_fnames.append(FITS_FNAME)

    context, log_fname = _prep_log_view(context, linear_reg_objs.log_msgs_list)
    html_fnames.append(log_fname)

    templates = _generate_template_fps(html_fnames)
    q2templates.render(templates, output_dir, context=context)


def view_log(output_dir: str, log: PysyndnaLogDirectoryFormat) -> None:
    log_list = pysyndna_log_directory_format_to_list(log)
    context, html_fname = _prep_log_view({}, log_list)
    templates = _generate_template_fps([html_fname])
    q2templates.render(templates, output_dir, context=context)


def _prep_log_view(context: dict, log: list) -> (dict, str):
    """
    Prepare the log view for rendering.

    Parameters
    ----------
    context : dict
        The context to be used in rendering the visualization.
    log : list
        The log messages to be written to the log file.

    Returns
    -------
    context : dict
        The context to be used in rendering the visualization, expanded with
        information pertaining to the log view.
    log_fname : str
        The name of the log view html (without path info).
    """

    context = _check_context(context)
    context[TABS_KEY].append({URL_KEY: LOG_FNAME, TITLE_KEY: 'Log'})
    context['log_msgs'] = log
    return context, LOG_FNAME


def _check_context(context: dict) -> dict:
    if not context:
        context = {}
    if TABS_KEY not in context:
        context[TABS_KEY] = []
    return context


def _generate_template_fps(html_fnames: list) -> list:
    if not INDEX_FNAME in html_fnames:
        html_fnames.append(INDEX_FNAME)
    return list(map(
        lambda page: os.path.join(TEMPLATES, page), html_fnames))
