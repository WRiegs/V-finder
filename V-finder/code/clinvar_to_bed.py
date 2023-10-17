import argparse

# Parse arguments using argparser
parser = argparse.ArgumentParser()

parser.add_argument("clinvar", help="clinvar variant summary file",
                    type=str)
parser.add_argument("--reference", help="NCBI36, GRCh37, GRCh38, supported",
                    type=str,
                    default="GRCh38",
                    required=False)

args = parser.parse_args()

def main(args):
    # Open the input and output files
    # Define the input and output file paths
    input_file_path = args.clinvar
    output_file_path = 'all_variants.bed'
    
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        # Process each line in the input file
        for line in input_file:
            # Skip lines starting with '#'
            if line.startswith('#'):
                continue
            
            # Split the line into columns
            columns = line.strip().split('\t')
            
            # Check the assembly column for
            assembly = columns[16]
            if assembly != args.reference:
                continue
            
            # Check if start and stop positions are valid integers
            start_value = columns[19]
            stop_value = columns[20]
            if not start_value.isdigit() or not stop_value.isdigit():
                continue
            
            start = int(start_value)
            stop = int(stop_value)

            ref_allele_vcf = columns[32]
            alt_allele_vcf = columns[33]
            
            # Skip entries with 'NA' values in columns 32 or 33
            if ref_allele_vcf == 'na' or alt_allele_vcf == 'na':
                continue
            
            # Skip entries with ref or alt allele lengths > 1:
            #if len(ref_allele_vcf) > 1 or len(alt_allele_vcf) > 1:
            #    continue
            
            chromosome = columns[18]
            
            if(start >= stop):
                continue

            # Add 'chr' prefix if not present
            if not chromosome.startswith('chr'):
                chromosome = 'chr' + chromosome

            # Format the BED line
            bed_line = f"{chromosome}\t{start - 1}\t{stop}\t{ref_allele_vcf}_{alt_allele_vcf}\t0\t+\n"
            
            # Write the BED line to the output file
            output_file.write(bed_line)


if __name__ == '__main__':
    main(args)