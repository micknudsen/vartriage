from typing import Iterable

from vartriage.core import VCF


def parse_vcf(stream: Iterable[str]) -> VCF:

    header = []
    columns = []
    data = []

    for row in stream:
        if row.startswith('##'):
            header.append(row)
        elif row.startswith('#'):
            columns.append(row)
        else:
            data.append(row)

    return VCF(header=header,
               columns=columns,
               data=data)
