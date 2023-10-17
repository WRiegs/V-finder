import argparse
import os

# Parse arguments using argparser
parser = argparse.ArgumentParser()

parser.add_argument("bed", help="bed file of transcription factor binding sites from remap2022 database",
                    type=str)
parser.add_argument("--out_folder", help="Folder where to save the output files",
                    type=str,
                    default="cell_type_split",
                    required=False)

args = parser.parse_args()

def main(args):
    # Dictionary to store entries for each cell type
    cell_type_entries = {}

    # Read the input BED file
    with open(args.bed, 'r') as bed_file:
        for line in bed_file:
            fields = line.strip().split('\t')
            if len(fields) >= 4:
                cell_type = fields[3].split('.')[2]  # Extract Cell_type
                if cell_type not in cell_type_entries:
                    cell_type_entries[cell_type] = []
                cell_type_entries[cell_type].append(line)

    # Write separate BED files for each cell type
    os.system(f'mkdir -p {args.out_folder}')	
    for cell_type, entries in cell_type_entries.items():
        output_filename = os.path.join(args.out_folder, f'{cell_type}.bed')
        with open(output_filename, 'w') as output_file:
            output_file.writelines(entries)
        print(f'Saved {len(entries)} entries for Cell_type {cell_type} in {output_filename}')
        

if __name__ == '__main__':
    main(args)