from typing import Dict, List, Set

from vartriage.core import Variant, VCF


class Triager:

    def __init__(self, evidence: Dict[str, List[Variant]]) -> None:

        self._evidence: Dict[str, Set[Variant]] = {}
        for evidence_id, evidence_variants in evidence.items():
            self._evidence[evidence_id] = set(variant for variant in evidence_variants if not variant.is_filtered())

    def triage(self, vcf: VCF) -> None:

        vcf.add_info_field(id_='VTSO', number='.', type_='String', description='Variant considered PASS based on second opinion from these callers (vartriage)')
        vcf.add_info_field(id_='VTOF', number='.', type_='String', description='Original FILTER before second opinion (vartriage)')

        for variant in vcf.variants:

            if variant.is_filtered():

                second_opinions = []

                for evidence_id, evidence_variants in self._evidence.items():
                    if variant in evidence_variants:
                        second_opinions.append(evidence_id)

                if second_opinions:
                    variant.set_info('VTSO', ','.join(second_opinions))
                    variant.set_info('VTOF', variant.filter_.replace(';', ','))
                    variant.filter_ = 'PASS'
