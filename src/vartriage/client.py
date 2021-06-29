import gzip

from typing import Dict, List

from argparse import ArgumentParser
from vartriage.core import Variant

from vartriage.parser import parse_vcf
from vartriage.triager import Triager


def main():

    parser = ArgumentParser()

    parser.add_argument('--triage_vcf_file', required=True, help='VCF file to be triaged')
    parser.add_argument('--evidence_vcf_files', required=True, help='Comma-separated list of ID:VCF_PATH evidence VCF files')

    args = parser.parse_args()

    with gzip.open(args.triage_vcf_file, 'rt') as f:
        vcf = parse_vcf(f)

    evidence: Dict[str, List[Variant]] = {}
    for vcf_id, vcf_file in [id_file_pair.split(':') for id_file_pair in args.evidence_vcf_files.split(',')]:
        with gzip.open(vcf_file, 'rt') as f:
            evidence[vcf_id] = parse_vcf(f).variants

    triager = Triager(evidence=evidence)
    triager.triage(vcf=vcf)

    for row in vcf.header:
        print(row)

    print('\t'.join(['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT'] + vcf.sample_names))

    for variant in vcf.variants:
        print(variant)
