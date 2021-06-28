from dataclasses import dataclass
from typing import Dict, List

from vartriage.exceptions import VariantException


@dataclass
class Variant():

    chrom: str
    pos: str
    id_: str
    ref: str
    alt: str
    qual: str
    filter_: str
    info: str
    format_: str
    samples: Dict[str, str]

    def __post_init__(self):
        if len(self.alt.split(',')) > 1:
            raise VariantException('Multiallelic variants are not supported. '
                                   'Please normalize input VCF files (e.g. using bcftools norm).')

    def is_filtered(self) -> bool:
        return not self.filter_ == 'PASS'


class VCF():

    def __init__(self, header: List[str], sample_names: List[str], data: List[str]):

        self._header = header
        self._sample_names = sample_names

        self._variants = []
        for row in data:
            chrom, pos, id_, ref, alt, qual, filter_, info, format_, *samples = row.split('\t')
            self._variants.append(
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


#     def __eq__(self, other: object) -> bool:
#         if not isinstance(other, Variant):
#             return NotImplemented
#         return all([self.chromosome == other.chromosome,
#                     self.position == other.position,
#                     self.ref == other.ref,
#                     self.alt == other.alt])

#     def __repr__(self):
#         parts = [self.chromosome, str(self.position), self.id, self.ref, self.alt, self.qual, self.filter, self.info]
#         if self.genotypes:
#             parts += self.genotypes
#         return '\t'.join(parts)

#     def is_filtered(self) -> bool:
#         return not self.filter == 'PASS'
