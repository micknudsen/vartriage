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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Variant):
            return NotImplemented
        return all([self.chrom == other.chrom,
                    self.pos == other.pos,
                    self.ref == other.ref,
                    self.alt == other.alt])

    def __repr__(self):
        parts = [self.chrom, self.pos, self.id_, self.ref, self.alt, self.qual, self.filter_, self.info, self.format_]
        parts += self.samples.values()
        return '\t'.join(parts)

    def is_filtered(self) -> bool:
        return not self.filter_ == 'PASS'


@dataclass
class VCF():

    header: List[str]
    sample_names: List[str]
    variants: List[Variant]

    def add_info_field(self, id_: str, number: str, type_: str, description: str) -> None:
        self.header.append(f'##<INFO=<ID={id_},Number={number},Type={type_},Description="{description}">')
