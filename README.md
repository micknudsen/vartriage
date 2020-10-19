![CI](https://github.com/micknudsen/vartriage/workflows/CI/badge.svg)

# vartriage

Just a little tool to perform second opinions on variant calls. It takes as input a `TRIAGE_VCF` and a list of `EVIDENCE_VCFS` and outputs a re-filtered version of `TRIAGE_VCF`, where filtered variants are reverted to `PASS` if they appear as `PASS` in one of the `EVIDENCE_VCFS`.

```
$vartriage --help
usage: vartriage [-h] --triage_vcf TRIAGE_VCF --evidence_vcfs EVIDENCE_VCFS

optional arguments:
  -h, --help            show this help message and exit
  --triage_vcf TRIAGE_VCF
                        VCF file to be triaged
  --evidence_vcfs EVIDENCE_VCFS
                        Comma-separated list of VCF files to be used as second opinions
```

A typical use-case could be to use Strelka as second opinion to Mutect2.

```
vartriage --triage_vcf mutect2.vcf.gz --evidence_vcfs strelka.snvs.vcf.gz,strelka.indels.vcf.gz | bgzip -c > triaged.vcf.gz
```

Note that multi-allelic variants are not supported by `vartriage`. It is thus recommended to first process input VCF files using `bcftools -m- foo.vcf.gz`, which splits multi-allelic variants into biallelic variants.

The recommended way to install `vartriage` is by using conda:
```
conda install -c micknudsen vartriage
```
