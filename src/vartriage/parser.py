from typing import Iterable

from vartriage.core import VCF


def parse_vcf(stream: Iterable[str]) -> VCF:

    header = []
    samples = []
    data = []

    for row in stream:
        if row.startswith('##'):
            header.append(row)
        elif row.startswith('#'):
            samples = row.split('\t')[9:]
        else:
            data.append(row)

    return VCF(header=header,
               samples=samples,
               data=data)
