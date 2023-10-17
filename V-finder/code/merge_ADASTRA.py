import os
import pandas as pd

# Specify the directory containing the TSV files
directory_path = 'ADASTRA_snvs_cltf/data'

# Initialize an empty list to store data from all files
data = []

# Iterate through the files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".tsv"):
        # Parse the relevant information from the file name
        parts = filename.split('@')
        tf_species = (parts[0].split('_'))[0]
        cell_type_tissue = parts[1].split('__')
        
        # If there's a cell type specified in the file name
        if len(cell_type_tissue) == 2:
            cell_type = cell_type_tissue[0]
            tissue = cell_type_tissue[1].rstrip('.tsv')
        else:
            cell_type = None  # Or any default value you prefer
            tissue = cell_type_tissue[0].rstrip('.tsv')
        
        # Read the TSV file into a DataFrame
        file_path = os.path.join(directory_path, filename)
        df = pd.read_csv(file_path, delimiter='\t')
        
        # Add the new columns
        df['Cell_type'] = cell_type
        df['TF'] = tf_species
        df['Tissue'] = tissue
        
        # Append the DataFrame to the list
        data.append(df)

# Concatenate all DataFrames into one
merged_data = pd.concat(data, ignore_index=True)

# Save the merged data to a new TSV file
output_file = 'ADASTRA_snvs_cltf/merged_cltf.tsv'
merged_data.to_csv(output_file, sep='\t', index=False)

print("Merged data saved to:", output_file)