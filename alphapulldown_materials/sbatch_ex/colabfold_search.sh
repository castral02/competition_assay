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

INPUT_DIR=""   # change to your directory

# Create individual features
create_individual_features.py --fasta_paths=$INPUT_DIR/bait.fasta,$INPUT_DIR/candidate.fasta --output_dir=$INPUT_DIR/pulldown_cf_msas --use_precomputed_msas=True --max_template_date=2023-01-01 --use_mmseqs2=True --skip_existing=True
