import unittest

from vartriage.core import Variant
from vartriage.core import Triager

from vartriage.exception import VariantException

from vartriage.parser import parse_vcf_entry


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


#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  Sera-K_Cardiomyo_1_2020-07-28_Exom_v3_val       Sera-K_Tumor_2020-07-28_Exom_v3_val

class TestParser(unittest.TestCase):

    def test_parse_variant(self):
        vcf_entry = '\t'.join(['chr5', '178575044', '.', 'AC', 'A', ',', 'PASS', 'AS_FilterStatus=SITE;AS_SB_TABLE=18,152|0,4;DP=176;ECNT=3;GERMQ=93;MBQ=32,36;MFRL=286,178;MMQ=60,60;MPOS=3;NALOD=1.58;NLOD=10.82;POPAF=6.00;ROQ=93;TLOD=15.39', 'GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB', '0|0:39,0:0.026:39:22,0:16,0:0|1:178575029_CAGAA_C:178575029:7,32,0,0', '0|1:131,4:0.039:135:57,3:65,1:0|1:178575029_CAGAA_C:178575029:11,120,0,4'])
        variant = parse_vcf_entry(entry=vcf_entry)
        self.assertEqual(variant.chromosome, 'chr5')
        self.assertEqual(variant.position, 178575044)
        self.assertEqual(variant.ref, 'AC')
        self.assertEqual(variant.alt, 'A')
        self.assertEqual(variant.qual, '.')
        self.assertEqual(variant.filter, 'PASS')
        self.assertEqual(variant.info, 'AS_FilterStatus=SITE;AS_SB_TABLE=18,152|0,4;DP=176;ECNT=3;GERMQ=93;MBQ=32,36;MFRL=286,178;MMQ=60,60;MPOS=3;NALOD=1.58;NLOD=10.82;POPAF=6.00;ROQ=93;TLOD=15.39')
        self.assertEqual(variant.format, 'GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB')
        self.assertEqual(variant.samples, ['0|0:39,0:0.026:39:22,0:16,0:0|1:178575029_CAGAA_C:178575029:7,32,0,0', '0|1:131,4:0.039:135:57,3:65,1:0|1:178575029_CAGAA_C:178575029:11,120,0,4'])


class TestTriager(unittest.TestCase):

    def setUp(self):

        evidence_vcf_entries = ['\t'.join(['chr1', '9611912', '.', 'A', 'T', '.', 'LowEVS', 'SOMATIC;QSS=2;TQSS=1;NT=het;QSS_NT=2;TQSS_NT=1;SGT=AA->AA;DP=341;MQ=59.86;MQ0=0;ReadPosRankSum=-5.89;SNVSB=28.56;SomaticEVS=0.00', 'DP:FDP:SDP:SUBDP:AU:CU:GU:TU', '68:9:0:0:41,43:3,3:0,0:15,22', '273:28:0:0:190,193:4,6:0,2:51,72']),
                                '\t'.join(['chr9', '129439117', '.', 'T', 'C', '.', 'PASS', 'SOMATIC;QSS=34;TQSS=2;NT=ref;QSS_NT=34;TQSS_NT=2;SGT=TT->CT;DP=101;MQ=60.00;MQ0=0;ReadPosRankSum=-0.11;SNVSB=0.00;SomaticEVS=8.04', 'DP:FDP:SDP:SUBDP:AU:CU:GU:TU', '21:0:0:0:0,0:1,1:0,0:20,20', '80:12:0:0:0,0:19,30:0,0:49,50']),
                                '\t'.join(['chr15', '93301718', '.', 'G', 'T', '.', 'PASS', 'SOMATIC;QSS=35;TQSS=1;NT=ref;QSS_NT=35;TQSS_NT=1;SGT=GG->GT;DP=37;MQ=60.00;MQ0=0;ReadPosRankSum=0.78;SNVSB=0.00;SomaticEVS=9.32', 'DP:FDP:SDP:SUBDP:AU:CU:GU:TU', '9:0:0:0:0,0:0,0:9,9:0,0', '27:0:0:0:0,0:0,0:22,23:5,5']),
                                '\t'.join(['chr20', '30388785', '.', 'T', 'G', '.', 'LowEVS', 'SOMATIC;QSS=5;TQSS=2;NT=ref;QSS_NT=5;TQSS_NT=2;SGT=TT->GT;DP=91;MQ=40.91;MQ0=6;ReadPosRankSum=-0.02;SNVSB=0.00;SomaticEVS=0.09', 'DP:FDP:SDP:SUBDP:AU:CU:GU:TU', '9:0:0:0:0,0:0,0:0,0:9,18', '53:2:0:0:0,0:0,0:3,4:48,69'])]

        self.triager = Triager()

        for vcf_entry in evidence_vcf_entries:
            variant = parse_vcf_entry(entry=vcf_entry)
            self.triager.add_evidence(variant=variant)

    def test_triage_pass_variant_which_passes_in_evidence(self):
        variant = parse_vcf_entry(entry='\t'.join(['chr15', '93301718', '.', 'G', 'T', '.', 'PASS', 'AS_FilterStatus=SITE;AS_SB_TABLE=0,31|0,5;DP=37;ECNT=1;GERMQ=42;MBQ=36,36;MFRL=289,327;MMQ=60,60;MPOS=22;NALOD=1.000;NLOD=2.71;POPAF=6.00;ROQ=81;TLOD=13.99', 'GT:AD:AF:DP:F1R2:F2R1:SB', '0/0:9,0:0.091:9:4,0:5,0:0,9,0,0', '0/1:22,5:0.207:27:8,3:13,2:0,22,0,5']))
        self.assertTrue(self.triager.triage(variant=variant))

    def test_triage_pass_variant_which_fails_in_evidence(self):
        variant = parse_vcf_entry(entry='\t'.join(['chr20', '30388785', '.', 'T', 'G', '.', 'PASS', 'AS_FilterStatus=SITE;AS_SB_TABLE=1,52|0,3;DP=56;ECNT=3;GERMQ=93;MBQ=36,36;MFRL=372,351;MMQ=60,40;MPOS=27;NALOD=1.06;NLOD=3.01;POPAF=6.00;ROQ=64;TLOD=5.22', 'GT:AD:AF:DP:F1R2:F2R1:SB', '0/0:10,0:0.081:10:2,0:7,0:0,10,0,0', '0/1:43,3:0.085:46:19,2:24,1:1,42,0,3']))
        self.assertTrue(self.triager.triage(variant=variant))

    def test_triage_filtered_variant_which_passes_in_evidence(self):
        variant = parse_vcf_entry(entry='\t'.join(['chr9', '129439117', '.', 'T', 'C', '.', 'clustered_events;haplotype', 'AS_FilterStatus=SITE;AS_SB_TABLE=32,34|13,9;DP=88;ECNT=7;GERMQ=44;MBQ=20,27;MFRL=181,167;MMQ=60,60;MPOS=24;NALOD=1.15;NLOD=3.91;POPAF=6.00;ROQ=93;TLOD=88.10', 'GT:AD:AF:DP:F1R2:F2R1:PGT:PID:PS:SB', '0|0:19,0:0.067:19:13,0:6,0:0|1:129439117_T_C:129439117:10,9,0,0', '0|1:47,22:0.335:69:25,11:20,11:0|1:129439117_T_C:129439117:22,25,13,9']))
        self.assertTrue(self.triager.triage(variant=variant))

    def test_triage_filtered_variants_which_is_filtered_in_evidence(self):
        variant = parse_vcf_entry(entry='\t'.join(['chr1', '9611912', '.', 'A', 'T', '.', 'base_qual;normal_artifact;strand_bias;weak_evidence', 'AS_FilterStatus=weak_evidence,base_qual,strand_bias;AS_SB_TABLE=125,77|0,19;DP=244;ECNT=1;GERMQ=93;MBQ=28,8;MFRL=210,261;MMQ=60,60;MPOS=24;NALOD=1.56;NLOD=9.82;POPAF=6.00;ROQ=56;TLOD=3.31', 'GT:AD:AF:DP:F1R2:F2R1:SB', '0/0:36,4:0.027:40:16,1:16,0:25,11,0,4', '0/1:166,15:0.042:181:68,1:67,3:100,66,0,15']))
        self.assertFalse(self.triager.triage(variant=variant))
