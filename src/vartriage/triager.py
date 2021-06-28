from typing import Dict, List

from vartriage.core import Variant


class Triager:

    def __init__(self, evidence: Dict[str, List[Variant]]) -> None:
        self._evidence = evidence
