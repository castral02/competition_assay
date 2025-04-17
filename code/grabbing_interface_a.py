import pandas as pd
import numpy as np
import json

#--------------- grabbing json file ----------------#
path_json = input("Path to json file: ")
with open(path_json, 'r') as file:
    data = json.load(file)

#--------------- For all the 1D Arrays Identifying Chain Residue ----------------#
residues = {'A': [], 'B': []} #the actual residue number
indices = {'A': [], 'B': []} #where it is indexed in the array from AF3
plddt = {'A': [], 'B': []}

for i, (chain_id, res_id, plddt_id) in enumerate(zip(data['token_chain_ids'], data['token_res_ids'], data['atom_plddts'])):
    if chain_id in residues:
        residues[chain_id].append(res_id)
        indices[chain_id].append(i)
        plddt[chain_id].append(plddt_id)

#--------------- Grabbing Contact Probs and PAE at Interface ----------------#
pae_matrix = np.array(data['pae'])
contact_matrix = np.array(data['contact_probs'])

contact_df = {'A Residue': [], 'B Residue': [], 'A PAE': [], 'B PAE': [], 
              'A Probability': [], 'B Probability': [], 'A plddt': [], 'B plddt': []}

for row_idx, col_idx in np.ndindex(pae_matrix.shape):  
    if row_idx in indices['A'] and col_idx in indices['B']:  
        a_prob = contact_matrix[row_idx, col_idx]  
        b_prob = contact_matrix[col_idx, row_idx]  

        a_pae = pae_matrix[row_idx, col_idx]  
        b_pae =  pae_matrix[col_idx, row_idx]  

        if a_prob > 0.1 and b_prob > 0.1:  # Filtering condition  
            #if a_pae < 10 and b_pae < 10: 
                contact_df['A Residue'].append(residues['A'][indices['A'].index(row_idx)])  
                contact_df['B Residue'].append(residues['B'][indices['B'].index(col_idx)])  
                contact_df['A PAE'].append(pae_matrix[row_idx, col_idx])  
                contact_df['B PAE'].append(pae_matrix[col_idx, row_idx])  
                contact_df['A Probability'].append(a_prob)  
                contact_df['B Probability'].append(b_prob)
                contact_df['A plddt'].append(plddt['A'][indices['A'].index(row_idx)])
                contact_df['B plddt'].append(plddt['B'][indices['B'].index(col_idx)])  
 

#--------------- Making it into a Dataframe ----------------#
contact_df = pd.DataFrame(contact_df)

#--------------- Grabbing the Best Paired Residue ----------------#
idx = contact_df.groupby('B Residue')['B Probability'].idxmax()
result_df = contact_df.loc[idx]

idx_2 = result_df.groupby('A Residue')['A Probability'].idxmax()
result_df = result_df.loc[idx_2]


file = input('What do you want to name the file: ')
result_df.to_csv(f'/Users/castroverdeac/Desktop/codes_for_AF/competition_assay/interface/{file}.csv', index= False)

