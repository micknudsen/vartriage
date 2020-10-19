from dataclasses import dataclass
from typing import List, Optional

from vartriage.exceptions import VariantException


@dataclass
class Variant():
    chromosome: str
    position: int
    ref: str
    alt: str
    filter: str = '.'
    id: str = '.'
    qual: str = '.'
    info: str = '.'
    genotypes: Optional[List[str]] = None

    def __post_init__(self):
        if len(self.alt.split(',')) > 1:
            raise VariantException

    def __eq__(self, other: 'Variant') -> bool:
        return all([self.chromosome == other.chromosome,
                    self.position == other.position,
                    self.ref == other.ref,
                    self.alt == other.alt])

    def __repr__(self):
        parts = [self.chromosome, str(self.position), self.id, self.ref, self.alt, self.qual, self.filter, self.info]
        if self.genotypes:
            parts += self.genotypes
        return '\t'.join(parts)

    def is_filtered(self) -> bool:
        return not self.filter == 'PASS'
