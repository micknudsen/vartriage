from typing import Iterable

from vartriage.core import VCF


def parse_vcf(stream: Iterable[str]) -> VCF:

    header = []
    sample_names = []
    data = []

    for row in stream:
        if row.startswith('##'):
            header.append(row)
        elif row.startswith('#'):
            sample_names = row.split('\t')[9:]
        else:
            data.append(row)

    return VCF(header=header,
               sample_names=sample_names,
               data=data)
