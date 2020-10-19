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

    def test_variant_filter_status(self):
        filtered_variant = Variant(chromosome='chr2', position=74492353, ref='T', alt='TAGGGTAA', filter='clustered_events;haplotype')
        non_filtered_variant = Variant(chromosome='chr16', position='4203316', ref='T', alt='C', filter='PASS')
        self.assertTrue(filtered_variant.is_filtered())
        self.assertFalse(non_filtered_variant.is_filtered())
