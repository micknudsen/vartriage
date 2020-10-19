import unittest

from vartriage.parser import parse_vcf_entry


class TestParser(unittest.TestCase):

    def setUp(self):
        vcf_entry = '\t'.join(['chr5', '178575044', '.', 'AC', 'A', '.', 'PASS', 'AS_FilterStatus=SITE;AS_SB_TABLE=18,152|0,4;DP=176;ECNT=3;GERMQ=93;MBQ=32,36;MFRL=286,178;MMQ=60,60;MPOS=3;NALOD=1.58;NLOD=10.82;POPAF=6.00;ROQ=93;TLOD=15.39', 'GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB', '0|0:39,0:0.026:39:22,0:16,0:0|1:178575029_CAGAA_C:178575029:7,32,0,0', '0|1:131,4:0.039:135:57,3:65,1:0|1:178575029_CAGAA_C:178575029:11,120,0,4'])
        self.variant = parse_vcf_entry(entry=vcf_entry)

    def test_parse_variant(self):
        self.assertEqual(self.variant.chromosome, 'chr5')
        self.assertEqual(self.variant.position, 178575044)
        self.assertEqual(self.variant.id, '.')
        self.assertEqual(self.variant.ref, 'AC')
        self.assertEqual(self.variant.alt, 'A')
        self.assertEqual(self.variant.qual, '.')
        self.assertEqual(self.variant.filter, 'PASS')
        self.assertEqual(self.variant.info, 'AS_FilterStatus=SITE;AS_SB_TABLE=18,152|0,4;DP=176;ECNT=3;GERMQ=93;MBQ=32,36;MFRL=286,178;MMQ=60,60;MPOS=3;NALOD=1.58;NLOD=10.82;POPAF=6.00;ROQ=93;TLOD=15.39')
        self.assertEqual(self.variant.genotypes, ['GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB', '0|0:39,0:0.026:39:22,0:16,0:0|1:178575029_CAGAA_C:178575029:7,32,0,0', '0|1:131,4:0.039:135:57,3:65,1:0|1:178575029_CAGAA_C:178575029:11,120,0,4'])
