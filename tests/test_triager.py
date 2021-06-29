import unittest

from vartriage.core import Variant, VCF
from vartriage.triager import Triager


class TestTriager(unittest.TestCase):

    def test_triage_filtered_variant_which_passes_in_evidence(self):

        vcf = VCF(
            header=[],
            sample_names=[],
            variants=[
                Variant(chrom='chr1', pos='100', id_='.', ref='A', alt='T', qual='.', filter_='clustered_events', info='', format_='', samples={})
            ]
        )

        triager = Triager(evidence={
            'X': [
                Variant(chrom='chr1', pos='100', id_='.', ref='A', alt='T', qual='.', filter_='PASS', info='', format_='', samples={})
            ]
        })

        triager.triage(vcf=vcf)

        self.assertFalse(vcf.variants[0].is_filtered())
        self.assertEqual(vcf.variants[0].get_info('VTSO'), 'X')
        self.assertEqual(vcf.variants[0].get_info('VTOF'), 'clustered_events')

    def test_triager_filtered_variant_which_is_also_filtered_in_evidence(self):

        vcf = VCF(
            header=[],
            sample_names=[],
            variants=[
                Variant(chrom='chr1', pos='100', id_='.', ref='A', alt='T', qual='.', filter_='clustered_events', info='', format_='', samples={})
            ]
        )

        triager = Triager(evidence={
            'X': [
                Variant(chrom='chr1', pos='100', id_='.', ref='A', alt='T', qual='.', filter_='LowEVS', info='', format_='', samples={})
            ]
        })

        triager.triage(vcf=vcf)

        self.assertTrue(vcf.variants[0].is_filtered())
        self.assertIs(vcf.variants[0].get_info('VTSO'), False)
        self.assertIs(vcf.variants[0].get_info('VTOF'), False)

    def test_triager_pass_variants_which_also_passes_in_evidence(self):

        vcf = VCF(
            header=[],
            sample_names=[],
            variants=[
                Variant(chrom='chr1', pos='100', id_='.', ref='A', alt='T', qual='.', filter_='PASS', info='', format_='', samples={})
            ]
        )

        triager = Triager(evidence={
            'X': [
                Variant(chrom='chr1', pos='100', id_='.', ref='A', alt='T', qual='.', filter_='haplotype', info='', format_='', samples={})
            ]
        })

        triager.triage(vcf=vcf)

        self.assertFalse(vcf.variants[0].is_filtered())
        self.assertIs(vcf.variants[0].get_info('VTSO'), False)
        self.assertIs(vcf.variants[0].get_info('VTOF'), False)

    def test_triager_pass_variants_which_fails_in_evidence(self):

        vcf = VCF(
            header=[],
            sample_names=[],
            variants=[
                Variant(chrom='chr1', pos='100', id_='.', ref='A', alt='T', qual='.', filter_='PASS', info='', format_='', samples={})
            ]
        )

        triager = Triager(evidence={
            'X': [
                Variant(chrom='chr1', pos='100', id_='.', ref='A', alt='T', qual='.', filter_='PASS', info='', format_='', samples={})
            ]
        })

        triager.triage(vcf=vcf)

        self.assertFalse(vcf.variants[0].is_filtered())
        self.assertIs(vcf.variants[0].get_info('VTSO'), False)
        self.assertIs(vcf.variants[0].get_info('VTOF'), False)

    def test_triager_multiple_variants_multiple_evidence(self):

        vcf = VCF(
            header=[],
            sample_names=[],
            variants=[
                Variant(chrom='chr1', pos='100', id_='.', ref='A', alt='T', qual='.', filter_='PASS', info='', format_='', samples={}),
                Variant(chrom='chr2', pos='500', id_='.', ref='G', alt='GATATA', qual='.', filter_='weak_evidence', info='', format_='', samples={}),
                Variant(chrom='chr3', pos='7500', id_='.', ref='ACT', alt='A', qual='.', filter_='germline', info='', format_='', samples={}),
                Variant(chrom='chr4', pos='1980', id_='.', ref='GGGG', alt='G', qual='.', filter_='haplotype', info='', format_='', samples={}),
                Variant(chrom='chr5', pos='5700', id_='.', ref='CTCTCT', alt='C', qual='.', filter_='slippage', info='', format_='', samples={}),
            ]
        )

        triager = Triager(evidence={
            'X': [
                Variant(chrom='chr2', pos='500', id_='.', ref='G', alt='GATATA', qual='.', filter_='PASS', info='', format_='', samples={}),
                Variant(chrom='chr3', pos='7500', id_='.', ref='ACT', alt='A', qual='.', filter_='contamination', info='', format_='', samples={})
            ],
            'Y': [
                Variant(chrom='chr2', pos='500', id_='.', ref='G', alt='GATATA', qual='.', filter_='PASS', info='', format_='', samples={}),
                Variant(chrom='chr4', pos='1980', id_='.', ref='GGGG', alt='G', qual='.', filter_='PASS', info='', format_='', samples={}),
            ]
        })

        triager.triage(vcf=vcf)

        self.assertFalse(vcf.variants[0].is_filtered())
        self.assertIs(vcf.variants[0].get_info('VTSO'), False)
        self.assertIs(vcf.variants[0].get_info('VTOF'), False)

        self.assertFalse(vcf.variants[1].is_filtered())
        self.assertEqual(vcf.variants[1].get_info('VTSO'), 'X,Y')
        self.assertEqual(vcf.variants[1].get_info('VTOF'), 'weak_evidence')

        self.assertTrue(vcf.variants[2].is_filtered())
        self.assertIs(vcf.variants[2].get_info('VTSO'), False)
        self.assertIs(vcf.variants[2].get_info('VTOF'), False)

        self.assertFalse(vcf.variants[3].is_filtered())
        self.assertEqual(vcf.variants[3].get_info('VTSO'), 'Y')
        self.assertEqual(vcf.variants[3].get_info('VTOF'), 'haplotype')

        self.assertTrue(vcf.variants[4].is_filtered())
        self.assertIs(vcf.variants[4].get_info('VTSO'), False)
        self.assertIs(vcf.variants[4].get_info('VTOF'), False)
