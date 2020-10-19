import unittest

from vartriage.core import Variant


class TestVariant(unittest.TestCase):

    def test_create_variant(self):
        variant = Variant(chromosome='chr1', position=14626, ref='G', alt='C', filter='map_qual')
        self.assertEqual(variant.chromosome, 'chr1')
        self.assertEqual(variant.position, 14626)
        self.assertEqual(variant.ref, 'G')
        self.assertEqual(variant.alt, 'C')
        self.assertEqual(variant.filter, 'map_qual')
