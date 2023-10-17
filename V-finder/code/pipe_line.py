import argparse
import os

# example usage of this script:
# python code/pipe_line.py input_files/remap2022_TP53_all_macs2_hg38_v1_0.bed input_files/variant_summary.txt --reference GRCh38 --vcf_out results/TP53_TFBS.vcf --clean
# python code/pipe_line.py single_cell_split/SW480_0h_TNFa.bed input_files/variant_summary.txt --reference GRCh38 --out_folder results --clean


# Parse arguments using argparser
parser = argparse.ArgumentParser()

parser.add_argument("bed", help="bed file of transcription factor binding sites",
                    type=str)
parser.add_argument("clinvar", help="clinvar variant summary file",
                    type=str)
parser.add_argument("--reference", help="NCBI36, GRCh37, GRCh38, supported",
                    type=str,
                    default="GRCh38",
                    required=False)
parser.add_argument("--vcf_out", help="vcf file of all single nucleotide variants",
                    type=str,
                    default="results/vcf_output_filtered.vcf",
                    required=False)
parser.add_argument("--clean", help="clean up intermediate files",
                    action='store_true',
                    default=False,
                    required=False)

args = parser.parse_args()


def main(args):
    # convert variant summary file to bed file
    # it will filter out variants that are not your specified human reference
    os.system("python code/clinvar_to_bed.py " + args.clinvar + " --reference " + args.reference)
    
    # prepare a vcf file of all single nucleotide variants
    os.system("python code/clinvar_to_vcf.py " + args.clinvar + " --reference " + args.reference)   
    
    # Intersect the two bed files, but for regions
    os.system("touch intersect_regions.bed")
    os.system("bedtools intersect -a " + args.bed + " -b all_variants.bed -wa > intersect_regions.bed")
    
    # Intersect the two bed files, but for variants
    os.system("touch intersect_variants.bed")
    os.system("bedtools intersect -a all_variants.bed -b intersect_regions.bed -wa > intersect_variants.bed")
    
    # deduplicate the intersected bed file
    os.system("awk '!a[$0]++' intersect_regions.bed > intersect_regions_deduplicated.bed")
    os.system("awk '!a[$0]++' intersect_variants.bed > intersect_variants_deduplicated.bed")
    
    # Now Filter the vcf file
    os.system("python code/vcf_filter_with_bed.py " + "intersect_variants_deduplicated.bed" + " all_variants.vcf" + " --vcf_out " + args.vcf_out)
    
    #Now you have a filtered vcf file you can use in Fabian!
    
    if args.clean is True:
        os.system("rm intersect*")
        os.system("rm all_variants*")
    
if __name__ == "__main__":
    main(args)