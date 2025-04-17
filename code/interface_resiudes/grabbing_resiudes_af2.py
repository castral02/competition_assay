import pickle
import numpy as np
import pandas as pd
from Bio.PDB import PDBParser
from scipy.spatial import distance_matrix

#---------------- Load Pickle -------------------#
path_pickle = input("Path to Pickle: ")
with open(path_pickle, "rb") as file:
    data = pickle.load(file)

#---------------- Load PDB -------------------#
parser = PDBParser(QUIET=True)
path_pdb = input("Path to PDB: ")
structure = parser.get_structure("model", path_pdb)

#---------------- Mapping Resiude -------------------#
residue_to_idx = {}
idx_counter = 0
chain_residues = {'A': [], 'B': []}

for model in structure:
    for chain in model:
        chain_id = chain.get_id()
        if chain_id not in ['A', 'B']:
            continue
            
        for residue in chain:
            res_id = residue.id[1]
            residue_to_idx[(chain_id, res_id)] = idx_counter
            chain_residues[chain_id].append((res_id, residue))
            idx_counter += 1

#---------------- Figuring out Alpha Carbon Distance -------------------#
ca_atoms_A = []
ca_ids_A = []
for res_id, residue in chain_residues['A']:
    if 'CA' in residue:
        ca_atoms_A.append(residue['CA'].get_coord())
        ca_ids_A.append(res_id)

ca_atoms_B = []
ca_ids_B = []
for res_id, residue in chain_residues['B']:
    if 'CA' in residue:
        ca_atoms_B.append(residue['CA'].get_coord())
        ca_ids_B.append(res_id)

if ca_atoms_A and ca_atoms_B:
    ca_coords_A = np.array(ca_atoms_A)
    ca_coords_B = np.array(ca_atoms_B)
    dist_matrix = distance_matrix(ca_coords_A, ca_coords_B)
else:
    print("No C-alpha atoms found in one or both chains")
    exit()


INTERFACE_THRESHOLD = 8.0  

#---------------- Grabbing PAE and Plddt -------------------#
pae_matrix = np.array(data['predicted_aligned_error'])
plddt_scores = np.array(data['plddt'])

contact_data = []
for i, res_A in enumerate(ca_ids_A):
    for j, res_B in enumerate(ca_ids_B):
        if dist_matrix[i, j] <= INTERFACE_THRESHOLD:
            idx_A = residue_to_idx.get(('A', res_A))
            idx_B = residue_to_idx.get(('B', res_B))
            
            if idx_A is not None and idx_B is not None:
                pae_score = pae_matrix[idx_A, idx_B]
                
                contact_data.append({
                    'A Residue': res_A,
                    'B Residue': res_B,
                    'Distance': dist_matrix[i, j],
                    'PAE': pae_score,
                    'A pLDDT': plddt_scores[idx_A],
                    'B pLDDT': plddt_scores[idx_B]
                })

#---------------- Output -------------------#
if contact_data:
    contact_df = pd.DataFrame(contact_data)


contact_df = contact_df.sort_values(by='PAE')

file = input('File name: ')
contact_df.to_csv(f"/Users/castroverdeac/Desktop/codes_for_AF/competition_assay/interface/{file}_af2.csv", index=False) 

