import unittest

from vartriage.core import Variant
from vartriage.parser import parse_vcf_entry


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


class TestParser(unittest.TestCase):

    def test_parse_variant(self):
        vcf_entry = '\t'.join(['chr5', '178575044', '.', 'AC', 'A', ',', 'PASS', 'AS_FilterStatus=SITE;AS_SB_TABLE=18,152|0,4;DP=176;ECNT=3;GERMQ=93;MBQ=32,36;MFRL=286,178;MMQ=60,60;MPOS=3;NALOD=1.58;NLOD=10.82;POPAF=6.00;ROQ=93;TLOD=15.39', 'GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB', '0|0:39,0:0.026:39:22,0:16,0:0|1:178575029_CAGAA_C:178575029:7,32,0,0', '0|1:131,4:0.039:135:57,3:65,1:0|1:178575029_CAGAA_C:178575029:11,120,0,4'])
        variant = parse_vcf_entry(entry=vcf_entry)
        self.assertEqual(variant.chromosome, 'chr5')
        self.assertEqual(variant.position, 178575044)
        self.assertEqual(variant.ref, 'AC')
        self.assertEqual(variant.alt, 'A')
        self.assertEqual(variant.filter, 'PASS')
