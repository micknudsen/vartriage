from typing import Dict, List

from vartriage.core import Variant, VCF


class Triager:

    def __init__(self, evidence: Dict[str, List[Variant]]) -> None:
        self._evidence = evidence

    def triage(self, vcf: VCF) -> None:

        vcf.add_info_field(id_='VTSO', number='.', type_='Integer', description='Variant considered PASS based on second opinion from these callers (vartriage)')
        vcf.add_info_field(id_='VTOF', number='.', type_='String', description='Original FILTER before second opinion (vartriage)')

        for variant in vcf.variants:

            if variant.is_filtered():

                second_opinions = []

                for evidence_id, evidence_variants in self._evidence.items():

                    for variant_ in evidence_variants:
                        if not variant_.is_filtered() and variant_ == variant:
                            second_opinions.append(evidence_id)
                            break

                if second_opinions:

                    variant.set_info('VTSO', ','.join(second_opinions))
                    variant.set_info('VTOF', variant.filter_)

                    variant.filter_ = 'PASS'
