import argparse

# Parse arguments using argparser
parser = argparse.ArgumentParser()

parser.add_argument("clinvar", help="clinvar variant summary file",
                    type=str)
parser.add_argument("--reference", help="hg19, hg37, hg38 supported",
                    type=str,
                    default="hg38",
                    required=False)

args = parser.parse_args()

def main(args):
    
    input_file_path = args.clinvar
    output_file_path = 'all_variants.vcf'

    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        header = '##fileformat=VCFv4.3\n'  # VCF version
        header += '##INFO=<ID=Phenotype,Number=1,Type=String,Description="Phenotype information">\n'  # INFO field
        header += '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n'  # Column headers
        output_file.write(header)

        for line in input_file:
            if line.startswith('#'):
                continue  # Skip header lines
            fields = line.strip().split('\t')
            vcf_line = make_vcf_line(fields)
            if vcf_line is not None:
                output_file.write(vcf_line + '\n')


def make_vcf_line(fields):
    chrom = fields[18]
    ref = fields[17]
    pos = fields[19]
    rs_id = fields[9] if fields[9] != "." else "."
    ref = fields[32]
    alt = fields[33]
    quality = "."
    filter_status = "."
    info = "RS=" + rs_id + ";Phenotype=" + fields[14]
    
    assembly = fields[16]
    if assembly != args.reference:
        return None

    # Check if both REF and ALT are 1 bp in length
    if ref.upper() != "NA" and alt.upper() != "NA" and len(ref) < 2 and len(alt) < 2:
        vcf_line = '\t'.join([chrom, pos, rs_id, ref, alt, quality, filter_status, info])
        return vcf_line
    else:
        return None

if __name__ == '__main__':
    main(args)