import argparse
import os

# Parse arguments using argparser
parser = argparse.ArgumentParser()

parser.add_argument("bed", help="bed file of variants to filter",
                    type=str)
parser.add_argument("clinvar", help="clinvar variant summary file in VCF format!",
                    type=str)
parser.add_argument("--vcf_out", help="Name of vcf file of all single nucleotide variants",
                    type=str,
                    default="vcf_output_filtered.vcf",
                    required=False)

args = parser.parse_args()

def main(args):
    # Step 1: Read and store data from the .bed file
    bed_data = {}
    with open(args.bed, 'r') as bed_file:
        for line in bed_file:
            chromosome, start_position, end_position, variant, x, strand = line.strip().split('\t')
            bed_data[(chromosome, int(start_position))] = variant

    # Step 2: Read the VCF file and filter based on .bed data
    filtered_vcf_lines = []
    with open(args.clinvar, 'r') as vcf_file:
        for line in vcf_file:
            if line.startswith('#'):
                # Skip header lines in VCF
                continue

            chrom, pos, _, _, _, _, _, _ = line.strip().split('\t')
            position = int(pos) # Bed file positions start with +1
            
            # Change line, so that the position is -1
            line = line.replace(pos, str(position))

            # Check if the (chromosome, position) exists in the .bed data
            if ("chr"+str(chrom), position) in bed_data:
                filtered_vcf_lines.append(line)

    # Step 3: Process or store the filtered VCF lines as needed
    os.system('touch ' + args.vcf_out)
    with open(args.vcf_out, 'w') as output_file:
        output_file.write(''.join(filtered_vcf_lines))
        
        
if __name__ == "__main__":
    main(args)
    