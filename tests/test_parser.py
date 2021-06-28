import unittest

from vartriage.core import Variant
from vartriage.parser import parse_vcf


class TestParser(unittest.TestCase):

    def test_parse_vcf(self):

        vcf_header = [
            '##fileformat=VCFv4.2',
            '##FILTER=<ID=PASS,Description="Site contains at least one allele that passes filters">',
            '##FILTER=<ID=clustered_events,Description="Clustered events observed in the tumor">',
            '##FILTER=<ID=weak_evidence,Description="Mutation does not meet likelihood threshold">',
            '##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths for the ref and alt alleles in the order listed">',
            '##FORMAT=<ID=AF,Number=A,Type=Float,Description="Allele fractions of alternate alleles in the tumor">',
            '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">',
            '##INFO=<ID=DP,Number=1,Type=Integer,Description="Approximate read depth; some reads may have been filtered">',
            '##INFO=<ID=STR,Number=0,Type=Flag,Description="Variant is a short tandem repeat">',
            '##contig=<ID=chr1,length=248956422>'
        ]

        vcf_columns = [
            '\t'.join(['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'NORMAL', 'TUMOR'])
        ]

        vcf_data = [
            '\t'.join(['chr1', '14752', '.', 'G', 'A', '.', 'weak_evidence', 'DP=236', 'GT:AD:AF', '0/0:113,4:0.063', '0/1:113,4:0.063']),
            '\t'.join(['chr1', '1625272', '.', 'GC', 'G', '.', 'clustered_events;weak_evidence', 'DP=455;STR', 'GT:AD:AF', '0|0:224,3:0.015', '0|1:225,3:0.015']),
            '\t'.join(['chr1', '11117039', '.', 'C', 'A', '.', 'PASS', 'DP=264', 'GT:AD:AF', '0/0:128,0:9.577e-03', '0/1:99,33:0.204'])
        ]

        vcf_file_lines = vcf_header + vcf_columns + vcf_data

        vcf = parse_vcf(stream=vcf_file_lines)

        self.assertEqual(vcf._header, vcf_header)
        self.assertEqual(vcf._sample_names, ['NORMAL', 'TUMOR'])

        self.assertEqual(vcf._variants, [Variant(chrom='chr1', pos='14752', id_='.', ref='G', alt='A', qual='.', filter_='weak_evidence', info='DP=236', format_='GT:AD:AF', samples={'NORMAL': '0/0:113,4:0.063', 'TUMOR': '0/1:113,4:0.063'}),
                                         Variant(chrom='chr1', pos='1625272', id_='.', ref='GC', alt='G', qual='.', filter_='clustered_events;weak_evidence', info='', format_='GT:AD:AF', samples={'NORMAL': '0|0:224,3:0.015', 'TUMOR': '0|1:225,3:0.015'}),
                                         Variant(chrom='chr1', pos='11117039', id_='.', ref='C', alt='A', qual='.', filter_='PASS', info='', format_='GT:AD:AF', samples={'NORMAL': '0/0:128,0:9.577e-03', 'TUMOR': '0/1:99,33:0.204'})])
