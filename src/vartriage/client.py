# import gzip

# from typing import Dict, List

# from argparse import ArgumentParser
# from vartriage.core import Variant

# from vartriage.parser import parse_vcf
# from vartriage.triager import Triager


def main():

    pass

    # parser = ArgumentParser()

    # parser.add_argument('--triage_vcf_file', required=True, help='VCF file to be triaged')
    # parser.add_argument('--evidence_vcf_files', required=True, help='Comma-separated list of VCF files to be used as second opinions')

    # args = parser.parse_args()

    # evidence: Dict[str, List[Variant]] = {}
    # for evidence_vcf_file in args.evidence_vcf_files:
    #     with gzip.open(evidence_vcf_file, 'rt') as f:
    #         vcf = parse_vcf(evidence_vcf_file)

    # triager = Triager()

    # with gzip.open(args.triage_vcf, 'rt') as f:
    #     for line in f:
    #         if line.startswith('#'):
    #             print(line.rstrip('\n'))
    #         else:
    #             variant = parse_vcf_entry(entry=line.rstrip('\n'))
    #             if triager.triage(variant=variant):
    #                 variant.filter = 'PASS'
    #             print(variant)
