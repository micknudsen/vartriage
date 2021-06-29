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
