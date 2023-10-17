import pandas as pd
import glob
import argparse
import os

# Parse arguments using argparser
parser = argparse.ArgumentParser()

parser.add_argument("vcf_folder", help="Folder containing split VCF files",
                    type=str)
parser.add_argument("--out_file", help="Folder where to save the output files",
                    type=str,
                    default="results/merged.vcf",
                    required=False)

args = parser.parse_args()

def main(args):

    # Path to your split VCF files
    file_pattern = args.vcf_folder+'*.vcf'

    # List all VCF files that match the pattern
    vcf_files = glob.glob(file_pattern)

    # Initialize an empty list to store dataframes
    dfs = []

    # Loop through each VCF file and read it into a dataframe
    for vcf_file in vcf_files:
        tissue_name = vcf_file.split('/')[-1].replace('.vcf', '')

        if os.path.getsize(vcf_file) > 0:
            df = pd.read_csv(vcf_file, sep='\t', comment='#', header=None)
            df['Tissue'] = tissue_name
            dfs.append(df)

    # Concatenate dataframes vertically
    merged_df = pd.concat(dfs, ignore_index=True)

    # Rename columns if necessary
    # merged_df.columns = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'SAMPLE', 'Tissue']

    # Save merged dataframe to a new VCF file
    merged_vcf_file = args.out_file
    merged_df.to_csv(merged_vcf_file, sep='\t', index=False, header=False)
    
if __name__ == '__main__':
    main(args)