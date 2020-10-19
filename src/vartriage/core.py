from typing import List, NamedTuple, Optional


class Variant(NamedTuple):
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
