import unittest

from vartriage.core import Variant
from vartriage.exceptions import VariantException


class TestVariant(unittest.TestCase):

    def test_create_variant(self):
        variant = Variant(chromosome='chr1', position=14626, ref='G', alt='C', filter='map_qual')
        self.assertEqual(variant.chromosome, 'chr1')
        self.assertEqual(variant.position, 14626)
        self.assertEqual(variant.ref, 'G')
        self.assertEqual(variant.alt, 'C')
        self.assertEqual(variant.filter, 'map_qual')

    def test_variant_equality(self):
        variant = Variant(chromosome='chr16', position=4203316, ref='T', alt='C', filter='PASS')
        same_variant = Variant(chromosome='chr16', position=4203316, ref='T', alt='C', filter='PASS')
        self.assertEqual(variant, same_variant)

    def test_variant_equality_different_filter_status(self):
        variant = Variant(chromosome='chr16', position=4203316, ref='T', alt='C', filter='PASS')
        same_variant_but_filtered = Variant(chromosome='chr16', position=4203316, ref='T', alt='C', filter='low_qual')
        self.assertEqual(variant, same_variant_but_filtered)

    def test_variant_inequality(self):
        variant = Variant(chromosome='chr16', position=4203316, ref='T', alt='C', filter='PASS')
        other_variant = Variant(chromosome='chr1', position=14626, ref='G', alt='C', filter='map_qual')
        self.assertNotEqual(variant, other_variant)

    def test_variant_comparison_with_non_variant_object(self):
        variant = Variant(chromosome='chr16', position=4203316, ref='T', alt='C', filter='PASS')
        not_a_variant = 'chr16  4203316 T   C   PASS'
        self.assertNotEqual(variant, not_a_variant)

    def test_variant_filter_status(self):
        filtered_variant = Variant(chromosome='chr2', position=74492353, ref='T', alt='TAGGGTAA', filter='clustered_events;haplotype')
        non_filtered_variant = Variant(chromosome='chr16', position=4203316, ref='T', alt='C', filter='PASS')
        self.assertTrue(filtered_variant.is_filtered())
        self.assertFalse(non_filtered_variant.is_filtered())

    def test_creating_multiallelic_variant_raises_exception(self):
        with self.assertRaises(VariantException):
            Variant(chromosome='chr1', position=143464674, ref='ATT', alt='A,ATTT', filter='multiallelic;normal_artifact')

    def test_variant_to_string(self):
        variant = Variant(chromosome='chr15', position=93301718, id='.', ref='G', alt='T', qual='.', filter='PASS', info='AS_FilterStatus=SITE;AS_SB_TABLE=0,31|0,5;DP=37;ECNT=1;GERMQ=42;MBQ=36,36;MFRL=289,327;MMQ=60,60;MPOS=22;NALOD=1.000;NLOD=2.71;POPAF=6.00;ROQ=81;TLOD=13.99', genotypes=['GT:AD:AF:DP:F1R2:F2R1:SB', '0/0:9,0:0.091:9:4,0:5,0:0,9,0,0', '0/1:22,5:0.207:27:8,3:13,2:0,22,0,5'])
        self.assertEqual(variant.__repr__(), 'chr15	93301718	.	G	T	.	PASS	AS_FilterStatus=SITE;AS_SB_TABLE=0,31|0,5;DP=37;ECNT=1;GERMQ=42;MBQ=36,36;MFRL=289,327;MMQ=60,60;MPOS=22;NALOD=1.000;NLOD=2.71;POPAF=6.00;ROQ=81;TLOD=13.99	GT:AD:AF:DP:F1R2:F2R1:SB	0/0:9,0:0.091:9:4,0:5,0:0,9,0,0	0/1:22,5:0.207:27:8,3:13,2:0,22,0,5')
