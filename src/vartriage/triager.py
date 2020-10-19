from typing import List

from vartriage.core import Variant


class Triager:

    def __init__(self) -> None:
        self._evidence: List[Variant] = []

    def add_evidence(self, variant: Variant) -> None:
        if not variant.is_filtered():
            self._evidence.append(variant)

    def triage(self, variant) -> bool:
        return not variant.is_filtered() or variant in self._evidence
