from argparse import ArgumentParser


def main():

    parser = ArgumentParser()

    parser.add_argument('--triage_vcf', required=True)
    parser.add_argument('--evidence_vcfs', required=True)

    args = parser.parse_args()
