import importlib_resources
import os
import q2templates
import yaml

from q2_pysyndna._settings import __package_name__
from q2_pysyndna._type_format_pysyndna_log import PysyndnaLogDirectoryFormat, \
    extract_fp_from_directory_format, load_list_from_pysyndnalog_fp, \
    extract_list_from_pysyndnalogdir_format
from q2_pysyndna._type_format_linear_regressions import \
    LinearRegressionsDirectoryFormat, \
    load_and_validate_linearregressionsyaml_fp

LOG_FNAME = 'log.html'
FITS_FNAME = 'fits.html'
INDEX_FNAME = 'index.html'
TABS_KEY = 'tabs'
URL_KEY = 'url'
TITLE_KEY = 'title'

REF = importlib_resources.files(__package_name__) / 'assets'
# NB: this method is not robust to files inside zips; see
# https://importlib-resources.readthedocs.io/en/latest/migration.html#pkg-resources-resource-filename
with importlib_resources.as_file(REF) as path:
    TEMPLATES = str(path)


def view_fit(output_dir: str,
             linear_regressions: LinearRegressionsDirectoryFormat) -> None:
    html_fnames = []
    context = _check_context({})

    linregs_fp = extract_fp_from_directory_format(
        linear_regressions, linear_regressions.linregs_yaml)
    linregs_dict = load_and_validate_linearregressionsyaml_fp(linregs_fp)

    log_fp = extract_fp_from_directory_format(
        linear_regressions, linear_regressions.log)
    logs_list = load_list_from_pysyndnalog_fp(log_fp)

    linregs_yaml_str = yaml.dump(linregs_dict)
    context['linregs_yaml'] = linregs_yaml_str
    context[TABS_KEY].append({URL_KEY: FITS_FNAME, TITLE_KEY: 'Fits'})
    html_fnames.append(FITS_FNAME)

    context, log_fname = _prep_log_view(context, logs_list)
    html_fnames.append(log_fname)

    templates = _generate_template_fps(html_fnames)
    q2templates.render(templates, output_dir, context=context)


def view_log(output_dir: str, log: PysyndnaLogDirectoryFormat) -> None:
    log_list = extract_list_from_pysyndnalogdir_format(log)
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
