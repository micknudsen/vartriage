from typing import Dict, List

from vartriage.core import Variant, VCF


class Triager:

    def __init__(self, evidence: Dict[str, List[Variant]]) -> None:
        self._evidence = evidence

    def triage(self, vcf: VCF) -> VCF:

        vcf.add_info_field(id_='VTSO',
                           number='.',
                           type_='Integer',
                           description='Variant considered PASS based on second opinion from these callers (vartriage)')

        vcf.add_info_field(id_='VTOF',
                           number='.',
                           type_='String',
                           description='Original FILTER before second opinion (vartriage)')
