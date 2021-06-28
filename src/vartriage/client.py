import gzip

from typing import Dict, List

from argparse import ArgumentParser
from vartriage.core import Variant

from vartriage.parser import parse_vcf
from vartriage.triager import Triager


def main():

    parser = ArgumentParser()

    parser.add_argument('--triage_vcf_file', required=True, help='VCF file to be triaged')
    parser.add_argument('--evidence_vcf_files', required=True)  # TODO: Add help here!

    args = parser.parse_args()

    evidence: Dict[str, List[Variant]] = {}
    for vcf_id, vcf_file in [id_file_pair.split(':') for id_file_pair in args.evidence_vcf_files.split(',')]:
        with gzip.open(vcf_file, 'rt') as f:
            evidence[vcf_id] = parse_vcf(f).variants

    triager = Triager(evidence=evidence)

    with gzip.open(args.triage_vcf_file, 'rt') as f:
        triager.triage(vcf=parse_vcf(f))

    #     for line in f:
    #         if line.startswith('#'):
    #             print(line.rstrip('\n'))
    #         else:
    #             variant = parse_vcf_entry(entry=line.rstrip('\n'))
    #             if triager.triage(variant=variant):
    #                 variant.filter = 'PASS'
    #             print(variant)
