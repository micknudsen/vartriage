from dataclasses import dataclass
from typing import List, Optional


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

    def is_filtered(self) -> bool:
        return not self.filter == 'PASS'
