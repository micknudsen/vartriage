# import gzip

# from argparse import ArgumentParser

# from vartriage.parser import parse_vcf_entry
# from vartriage.triager import Triager


def main():

    pass

    # parser = ArgumentParser()

    # parser.add_argument('--triage_vcf', required=True, help='VCF file to be triaged')
    # parser.add_argument('--evidence_vcfs', required=True, help='Comma-separated list of VCF files to be used as second opinions')

    # args = parser.parse_args()

    # triager = Triager()

    # for evidence_vcf in args.evidence_vcfs.split(','):
    #     with gzip.open(evidence_vcf, 'rt') as f:
    #         for line in f:
    #             if not line.startswith('#'):
    #                 variant = parse_vcf_entry(entry=line.rstrip('\n'))
    #                 triager.add_evidence(variant=variant)

    # with gzip.open(args.triage_vcf, 'rt') as f:
    #     for line in f:
    #         if line.startswith('#'):
    #             print(line.rstrip('\n'))
    #         else:
    #             variant = parse_vcf_entry(entry=line.rstrip('\n'))
    #             if triager.triage(variant=variant):
    #                 variant.filter = 'PASS'
    #             print(variant)
