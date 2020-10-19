import gzip

from argparse import ArgumentParser

from vartriage.core import Variant
from vartriage.parser import parse_vcf_entry
from vartriage.triager import Triager


def main():

    parser = ArgumentParser()

    parser.add_argument('--triage_vcf', required=True)
    parser.add_argument('--evidence_vcfs', required=True)

    args = parser.parse_args()

    triager = Triager()

    for evidence_vcf in args.evidence_vcfs.split(','):
        with gzip.open(evidence_vcf, 'rt') as f:
            for line in f:
                if not line.startswith('#'):
                    variant = parse_vcf_entry(entry=line.rstrip('\n'))
                    triager.add_evidence(variant=variant)
