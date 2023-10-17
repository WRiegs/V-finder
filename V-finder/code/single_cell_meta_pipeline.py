import argparse
import os

# example usage of this script:
# python code/single_cell_meta_pipeline.py input_files/remap2022_TP53_all_macs2_hg38_v1_0.bed input_files/variant_summary.txt --reference GRCh38 --out_folder results --clean

# Parse arguments using argparser
parser = argparse.ArgumentParser()

parser.add_argument("bed", help="bed file of transcription factor binding sites from remap2022 database",
                    type=str)
parser.add_argument("clinvar", help="clinvar variant summary file",
                    type=str)
parser.add_argument("--celltype_bed_folder", help="Folder where to save the output files",
                    type=str,
                    default="cell_type_split",
                    required=False)
parser.add_argument("--reference", help="NCBI36, GRCh37, GRCh38, supported",
                    type=str,
                    default="GRCh38",
                    required=False)
parser.add_argument("--out_folder", help="vcf file of all single nucleotide variants",
                    type=str,
                    default="results",
                    required=False)
parser.add_argument("--clean", help="clean up intermediate files",
                    action='store_true',
                    default=False,
                    required=False)

args = parser.parse_args()

def main(args):
    #TODO: convert VCF files here first and then run the pipeline
    
    #TODO: add checks for file formats in the parser?
    
    # run celltype splitter
    os.system("python code/remap_bed_celltype_splitter.py " + args.bed + " --out_folder " + args.celltype_bed_folder)
    
    # for every bed file in args.celltype_bed_folder, run the pipeline
    for filename in os.listdir(args.celltype_bed_folder):
        os.system("python code/pipe_line.py " + args.celltype_bed_folder + "/" + filename + " " + args.clinvar + " --reference " + args.reference + " --vcf_out " + args.out_folder + '/' + filename[:-3] + 'vcf' + " --clean")
        print("Finished search for variants in " + args.out_folder + '/' + filename[:-3] + 'vcf')
        
    os.system("python code/merge_tissue_beds.py " + args.out_folder + " " + args.out_folder + "/merged.vcf")
    
    # Okay... so I know it's very inefficient to do this,
    # It would have been best to merge the cell type beds first and then run the pipeline on the merged bed file.
    # But I don't have time to change it now.
    # It still works okay enough. 
    
if __name__ == '__main__':
    main(args)