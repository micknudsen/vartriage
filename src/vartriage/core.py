from dataclasses import dataclass
from typing import Dict, List, Optional, Union

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

    def get_info(self, key: str) -> Union[str, bool]:
        for entry in self.info.split(';'):
            if '=' in entry:
                key_, value_ = entry.split('=', 1)
                if key_ == key:
                    return value_
            else:
                if entry == key:
                    return True
        return False

    def set_info(self, key: str, value: Optional[str] = None) -> None:
        info_entries = self.info.split(';')
        for i, entry in enumerate(info_entries):
            key_ = entry.split('=')[0] if '=' in entry else entry
            if key_ == key:
                if value:
                    info_entries[i] = f'{key}={value}'
                else:
                    info_entries[i] = key
                self.info = ';'.join(info_entries)
                return
        if value:
            info_entries.append(f'{key}={value}')
        else:
            info_entries.append(key)
        self.info = ';'.join(info_entries)


@dataclass
class VCF():

    header: List[str]
    sample_names: List[str]
    variants: List[Variant]

    def add_info_field(self, id_: str, number: str, type_: str, description: str) -> None:
        self.header.append(f'##INFO=<ID={id_},Number={number},Type={type_},Description="{description}">')
