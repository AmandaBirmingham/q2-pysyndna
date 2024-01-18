from ._plugin import fit
from . import _version
__version__ = _version.get_versions()['version']

__name__ = 'q2-pysyndna'
__description__ = 'Plugin to calculate absolute microbial cell counts'
__long_description__ = ('This QIIME 2 plugin wraps pysyndna to calculate '
                        'absolute microbial cell counts from shotgun data '
                        'that includes synthetic DNA spike-ins.')
__license__ = 'BSD-3-Clause'
__author__ = 'Amanda Birmingham'
__email__ = 'abirmingham@ucsd.edu'
__url__ = 'https://github.com/AmandaBirmingham/q2-pysyndna'
__package__ = 'q2_pysyndna'

__all__ = ['fit']