#!/bin/bash
#SBATCH --job-name=colabfold_search      
#SBATCH --partition=norm                
#SBATCH --mem=200G                      
#SBATCH --cpus-per-task=16              
#SBATCH --gres=lscratch:50                        
#SBATCH --time=3-24:00:00                   
#SBATCH --output=output/colabfold_search.log    
#SBATCH --error=error/colabfold_search.log      
#SBATCH --mail-type=END,FAIL   
#SBATCH --mail-user=  # Replace with your email address

set -e
set -x  # Enable debugging

# Load necessary modules
module load colabfold alphapulldown/0.30.7

cd ""   # change to your directory

run_multimer_jobs.py     --mode=pulldown     --num_cycle=3     --num_predictions_per_model=2     --output_path=pulldown_models     --protein_lists=bait.txt,candidate.txt     --monomer_objects_dir=pulldown_cf_msas

run_get_good_pae.sh --output_dir pulldown_models --cutoff=50

source myconda 

conda activate myenv #or whatever environment you need

python3 ../lia_lis.py -output_dir=pulldown_models
