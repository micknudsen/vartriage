from vartriage.core import Variant


def parse_vcf_entry(entry: str) -> Variant:
    chromosome, position, id, ref, alt, qual, filter, info, *genotypes = entry.split('\t')
    return Variant(chromosome=chromosome,
                   position=int(position),
                   id=id,
                   ref=ref,
                   alt=alt,
                   qual=qual,
                   filter=filter,
                   info=info,
                   genotypes=genotypes)
