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
        variant = Variant(chromosome='chr16', position='4203316', ref='T', alt='C', filter='PASS')
        same_variant = Variant(chromosome='chr16', position='4203316', ref='T', alt='C', filter='PASS')
        self.assertEqual(variant, same_variant)

    def test_variant_equality_different_filter_status(self):
        variant = Variant(chromosome='chr16', position='4203316', ref='T', alt='C', filter='PASS')
        same_variant_but_filtered = Variant(chromosome='chr16', position='4203316', ref='T', alt='C', filter='low_qual')
        self.assertEqual(variant, same_variant_but_filtered)

    def test_variant_inequality(self):
        variant = Variant(chromosome='chr16', position='4203316', ref='T', alt='C', filter='PASS')
        other_variant = Variant(chromosome='chr1', position=14626, ref='G', alt='C', filter='map_qual')
        self.assertNotEqual(variant, other_variant)

    def test_variant_filter_status(self):
        filtered_variant = Variant(chromosome='chr2', position=74492353, ref='T', alt='TAGGGTAA', filter='clustered_events;haplotype')
        non_filtered_variant = Variant(chromosome='chr16', position='4203316', ref='T', alt='C', filter='PASS')
        self.assertTrue(filtered_variant.is_filtered())
        self.assertFalse(non_filtered_variant.is_filtered())

    def test_creating_multiallelic_variant_raises_exception(self):
        with self.assertRaises(VariantException):
            Variant(chromosome='chr1', position=143464674, ref='ATT', alt='A,ATTT', filter='multiallelic;normal_artifact')

    def test_variant_to_string(self):
        variant = Variant(chromosome='chr15', position=93301718, id='.', ref='G', alt='T', qual='.', filter='PASS', info='AS_FilterStatus=SITE;AS_SB_TABLE=0,31|0,5;DP=37;ECNT=1;GERMQ=42;MBQ=36,36;MFRL=289,327;MMQ=60,60;MPOS=22;NALOD=1.000;NLOD=2.71;POPAF=6.00;ROQ=81;TLOD=13.99', genotypes=['GT:AD:AF:DP:F1R2:F2R1:SB', '0/0:9,0:0.091:9:4,0:5,0:0,9,0,0', '0/1:22,5:0.207:27:8,3:13,2:0,22,0,5'])
        self.assertEqual(variant.__repr__(), 'chr5	178575044	.	AC	A	.	PASS	AS_FilterStatus=SITE;AS_SB_TABLE=18,152|0,4;DP=176;ECNT=3;GERMQ=93;MBQ=32,36;MFRL=286,178;MMQ=60,60;MPOS=3;NALOD=1.58;NLOD=10.82;POPAF=6.00;ROQ=93;TLOD=15.39	GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB	0|0:39,0:0.026:39:22,0:16,0:0|1:178575029_CAGAA_C:178575029:7,32,0,0	0|1:131,4:0.039:135:57,3:65,1:0|1:178575029_CAGAA_C:178575029:11,120,0,4')
