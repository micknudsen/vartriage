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

    def is_filtered(self) -> bool:
        return not self.filter == 'PASS'
