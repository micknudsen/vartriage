import unittest

from vartriage.core import Variant
# from vartriage.exceptions import VariantException


class TestVariant(unittest.TestCase):

    def test_variant_equality(self):
        variant = Variant(chrom='chr1', pos='14752', id_='.', ref='G', alt='A', qual='.', filter_='weak_evidence', info='DP=236', format_='GT:AD:AF', samples={'NORMAL': '0/0:113,4:0.063', 'TUMOR': '0/1:113,4:0.063'})
        same_variant = Variant(chrom='chr1', pos='14752', id_='.', ref='G', alt='A', qual='.', filter_='weak_evidence', info='DP=236', format_='GT:AD:AF', samples={'NORMAL': '0/0:113,4:0.063', 'TUMOR': '0/1:113,4:0.063'})
        self.assertEqual(variant, same_variant)

    def test_variant_equality_different_filter_status(self):
        variant = Variant(chrom='chr1', pos='14752', id_='.', ref='G', alt='A', qual='.', filter_='weak_evidence', info='DP=236', format_='GT:AD:AF', samples={'NORMAL': '0/0:113,4:0.063', 'TUMOR': '0/1:113,4:0.063'})
        same_variant_but_not_filtered = Variant(chrom='chr1', pos='14752', id_='.', ref='G', alt='A', qual='.', filter_='PASS', info='DP=236', format_='GT:AD:AF', samples={'NORMAL': '0/0:113,4:0.063', 'TUMOR': '0/1:113,4:0.063'})
        self.assertEqual(variant, same_variant_but_not_filtered)

    def test_variant_inequality(self):
        variant = Variant(chrom='chr1', pos='14752', id_='.', ref='G', alt='A', qual='.', filter_='weak_evidence', info='DP=236', format_='GT:AD:AF', samples={'NORMAL': '0/0:113,4:0.063', 'TUMOR': '0/1:113,4:0.063'})
        other_variant = Variant(chrom='chr1', pos='1625272', id_='.', ref='GC', alt='G', qual='.', filter_='clustered_events;weak_evidence', info='DP=455;STR', format_='GT:AD:AF', samples={'NORMAL': '0|0:224,3:0.015', 'TUMOR': '0|1:225,3:0.015'})
        self.assertNotEqual(variant, other_variant)

    def test_variant_comparison_with_non_variant_object(self):
        variant = Variant(chrom='chr1', pos='14752', id_='.', ref='G', alt='A', qual='.', filter_='weak_evidence', info='DP=236', format_='GT:AD:AF', samples={'NORMAL': '0/0:113,4:0.063', 'TUMOR': '0/1:113,4:0.063'})
        not_a_variant = 'chr1	14752	.	G	A	.	weak_evidence	DP=236	GT:AD:AF	0/0:113,4:0.063	0/1:113,4:0.063'
        self.assertNotEqual(variant, not_a_variant)

    def test_variant_filter_status(self):
        filtered_variant = Variant(chrom='chr1', pos='14752', id_='.', ref='G', alt='A', qual='.', filter_='weak_evidence', info='DP=236', format_='GT:AD:AF', samples={'NORMAL': '0/0:113,4:0.063', 'TUMOR': '0/1:113,4:0.063'})
        non_filtered_variant = Variant(chrom='chr1', pos='11117039', id_='.', ref='C', alt='A', qual='.', filter_='PASS', info='DP=264', format_='GT:AD:AF', samples={'NORMAL': '0/0:128,0:9.577e-03', 'TUMOR': '0/1:99,33:0.204'})
        self.assertTrue(filtered_variant.is_filtered())
        self.assertFalse(non_filtered_variant.is_filtered())

    def test_creating_multiallelic_variant_raises_exception(self):
        with self.assertRaises(VariantException):
            Variant(chrom='chr1', pos='8013449', id_='.', ref='C', alt='G,A', qual='.', filter_='clustered_events;multiallelic', info='DP=238', format_='GT:AD:AF', samples={'NORMAL': '0/0:113,2,0:0.030', 'TUMOR': '0/1/2:59,2,56:0.029,0.440'})

    def test_variant_to_string(self):
        variant = Variant(chrom='chr1', pos='14752', id_='.', ref='G', alt='A', qual='.', filter_='weak_evidence', info='DP=236', format_='GT:AD:AF', samples={'NORMAL': '0/0:113,4:0.063', 'TUMOR': '0/1:113,4:0.063'})
        self.assertEqual(variant.__repr__(), 'chr1	14752	.	G	A	.	weak_evidence	DP=236	GT:AD:AF	0/0:113,4:0.063	0/1:113,4:0.063')
