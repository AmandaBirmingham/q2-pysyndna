import unittest

import q2_pysyndna
from q2_pysyndna.plugin_setup import plugin as pysyndna_plugin


class PluginSetupTests(unittest.TestCase):

    def test_plugin_setup(self):
        self.assertEqual(pysyndna_plugin.name, q2_pysyndna.__plugin_name__)
