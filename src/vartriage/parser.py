from typing import Iterable, List

from vartriage.core import Variant, VCF


def parse_vcf(stream: Iterable[str]) -> VCF:

    header: List[str] = []
    sample_names: List[str] = []
    variants: List[Variant] = []

    for row in stream:
        if row.startswith('##'):
            header.append(row.rstrip('\n'))
        elif row.startswith('#'):
            sample_names = row.rstrip('\n').split('\t')[9:]
        else:
            chrom, pos, id_, ref, alt, qual, filter_, info, format_, *samples = row.rstrip('\n').split('\t')
            variants.append(
                Variant(chrom=chrom,
                        pos=pos,
                        id_=id_,
                        ref=ref,
                        alt=alt,
                        qual=qual,
                        filter_=filter_,
                        info=info,
                        format_=format_,
                        samples=dict(zip(sample_names, samples)))
            )

    return VCF(header=header,
               sample_names=sample_names,
               variants=variants)
