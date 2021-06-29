[![install with conda](https://anaconda.org/micknudsen/vartriage/badges/version.svg)](https://anaconda.org/micknudsen/vartriage) ![CI](https://github.com/micknudsen/vartriage/workflows/CI/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/micknudsen/vartriage/badge.svg?branch=master)](https://coveralls.io/github/micknudsen/vartriage?branch=master)

# vartriage

Just a little tool to perform second opinions on variant calls. It takes as input a _triage_ VCF file and list of _evidence_ VCF files. Output (written to `stdout`) is an opdated version of the _triage_ VCF, where filtered variants that `PASS` in any of the _evidence_ VCF files are marked as `PASS`.

```
$ vartriage --help
usage: vartriage [-h] --triage_vcf TRIAGE_VCF --evidence_vcfs EVIDENCE_VCFS

optional arguments:
  -h, --help            show this help message and exit
  --triage_vcf TRIAGE_VCF
                        VCF file to be triaged
  --evidence_vcfs EVIDENCE_VCFS
                        Comma-separated list of ID:VCF_PATH evidence VCF files
```

When a variant in un-filtered, two `INFO` fields are added in the output VCF file: `VTOF` contains the original filter reason before triage, and `VTSO` contains a comma-separated list of IDs of _evidence_ VCF files which support the second opinion.

Note that multi-allelic variants are not supported by `vartriage`. It is thus recommended to first process input VCF files using `bcftools norm -m- foo.vcf.gz`, which splits multi-allelic variants into biallelic variants.

# Example

A typical use-case could be to use Strelka as second opinion to Mutect2.

```
vartriage --triage_vcf mutect2.vcf.gz --evidence_vcfs STRELKA_SNV:strelka.snvs.vcf.gz,STRELKA_INDEL:strelka.indels.vcf.gz | bgzip -c > triaged.vcf.gz
```

For example, suppose that a variant in `mutect2.vcf.gz` is filtered:

```
chr17   39725187        .       C       T       .       clustered_events        AS_FilterStatus=SITE;AS_SB_TABLE=196,188|31,49;DP=472;ECNT=5;GERMQ=93;MBQ=35,20;MFRL=268,229;MMQ=60,60;MPOS=35;NALOD=2.30;NLOD=58.69;POPAF=6.00;ROQ=93;TLOD=190.21      GT:AD:AF:DP:F1R2:F2R1:SB        0/0:231,0:5.023e-03:231:115,0:116,0:113,118,0,0        0/1:153,80:0.306:233:74,41:79,39:83,70,31,49
```

If the same variant is called (but not filtered) in `strelka.snvs.vcf.gz`:

```
chr17   39725187        .       C       T       .       PASS    SOMATIC;QSS=333;TQSS=2;NT=ref;QSS_NT=3070;TQSS_NT=1;SGT=CC->CT;DP=466;MQ=60.00;MQ0=0;ReadPosRankSum=1.08;SNVSB=0.00;SomaticEVS=19.98    DP:FDP:SDP:SUBDP:AU:CU:GU:TU    232:0:0:0:0,0:232,232:0,0:0,0   232:0:0:0:0,0:151,153:0,0:81,81
```

The conclusion after triage is:

```
chr17   39725187        .       C       T       .       PASS    AS_FilterStatus=SITE;AS_SB_TABLE=196,188|31,49;DP=472;ECNT=5;GERMQ=93;MBQ=35,20;MFRL=268,229;MMQ=60,60;MPOS=35;NALOD=2.3;NLOD=58.69;POPAF=6;ROQ=93;TLOD=190.21;VTSO=STRELKA_SNV;VTOF=clustered_events   GT:AD:AF:DP:F1R2:F2R1:SB       0/0:231,0:0.005023:231:115,0:116,0:113,118,0,0  0/1:153,80:0.306:233:74,41:79,39:83,70,31,49
```

# Installation

The recommended way to install `vartriage` is by using conda:
```
$ conda install -c micknudsen vartriage
```
