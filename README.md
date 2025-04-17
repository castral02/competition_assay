# Competition Assay
This repository contains a python code for a simple scoring method in discovering highly interactive proteins using the AlphaPulldown Pipeline. 

## About
This code is a supplement to the research in the paper **Hierarchical small molecule inhibition of MYST acetyltransferases** ([Chen et. al, 2025]()). In our chemoproteomic experiments, we identified a new candidate member of these KAT complexes: FOXK2. As an initial experiment, and just the scratch of the surface, we wanted to understand FOXK2's ability to interact with MYST commplexes. In this code, we developed a simple scoring method in discovering new interactors in a high throughput computional competitive assay in finding the role of FOXK2 in the MYST complex. 

## AlphaPulldown Workflow
We implemented the [AlphaPulldown Workflow](https://academic.oup.com/bioinformatics/article/39/1/btac749/6839971) with the attachment of calculating the LIA and LIS which has been modified by the Enhanced Protein-Protein Interaction Discovery via AlphaFold-Multimer ([Kim et al., 2024](https://www.biorxiv.org/content/10.1101/2024.02.19.580970v1)) paper. 

We ran our AlphaPulldowns off the NIH HPC Biowulf Cluster. We used a ColabFold Search to find MSAs and used AlphaPulldown 0.30.7 to find the mpDockQ/pDockQ score. To look at how the folder should be organized, [click here](alphapulldown_materials/FOXK2_ex)

### How to run on the Biowulf cluster:

***ColabFold Search***
```bash
sinteractive --mem=128g --cpus-per-task=16 --gres=lscratch:100
module load colabfold alphapulldown/0.30.7
colabfold_search  --threads $SLURM_CPUS_PER_TASK for_colabfold.fasta $COLABFOLD_DB pulldown_cf_msas
create_individual_features.py --fasta_paths=bait.fasta,candidate.fasta --output_dir=pulldown_cf_msas --use_precomputed_msas=True --max_template_date=2023-01-01 --use_mmseqs2=True –skip_existing=True
```


***AlphaPulldown***
```bash
sinteractive --mem=150g -c8 --gres=lscratch:50,gpu:a100:1 --time=3-12:00:00
module load alphapulldown/0.30.7
run_multimer_jobs.py --mode=pulldown --num_cycle=3 --num_predictions_per_model=1 --output_path=pulldown_model --protein_lists=candidate.txt,bait.txt --monomer_objects_dir=pulldown_cf_msas
run_get_good_pae.sh --output_dir pulldown_model --cutoff=50
```

To look at the sbatch files, [click here](alphapulldown_materials/sbatch_ex).

### How to find LIA/LIS:
To find LIA/LIS, look at this [code](https://github.com/castral02/frag_af/blob/main/pipeline/lia_lis.py).

***How to run:***
```bash
python3 lia_lis.py -output_dir=/path/to/AlphaPulldown/output/folders
```

Example of an [output](alphapulldown_materials/alphapulldown_output.csv)

## Competition Assay 

### Developing Metrics
Previous research has a explored a multitidue of AlphaFold metrics in understanding protein-protien interactions. We wanted to develop a score that envelops popular metrics without denoting the confidence of one metric over the other. In this case, we decided to explore two major docking metrics: [mpDockQ/pDockQ](https://www.nature.com/articles/s41467-022-33729-4) and [LIA/LIS](https://www.biorxiv.org/content/10.1101/2024.02.19.580970v1). In the case of our metric, we filtered the metric according to minimum thresholds and depending how many are passed a consant score is given to the summation of the normalized score. Look below for a full workflow.

### Image of Workflow
![Alt Text](images/scheme.png)

### How to run: 
**Installation**

```bash
git clone https://github.com/castral02/competition_assay
cd code
python3 competition_assay.py -csv_path=/path/to/csv/file -name=Protein
```

## Dependencies 
```bash
absl-py
```

## Declaration of Generative AI Usage
This project utilized OpenAI's ChatGPT to assist in generating Python code, documentation, or other textual content.

## References
Bryant, P., Pozzati, G., Zhu, W. et al. Predicting the structure of large protein complexes using AlphaFold and Monte Carlo tree search. Nat Commun 13, 6028 (2022). [Paper Link](https://doi.org/10.1038/s41467-022-33729-4)

Dingquan Yu, Grzegorz Chojnowski, Maria Rosenthal, Jan Kosinski, AlphaPulldown—a python package for protein–protein interaction screens using AlphaFold-Multimer, Bioinformatics, Volume 39, Issue 1, (2023). [Paper Link](https://doi.org/10.1093/bioinformatics/btac749)

Kim AR, Hu Y, Comjean A, Rodiger J, Mohr SE, Perrimon N. "Enhanced Protein-Protein Interaction Discovery via AlphaFold-Multimer" bioRxiv (2024). [Paper Link](https://www.biorxiv.org/content/10.1101/2024.02.19.580970v1)

This work utilized the computational resources of the [NIH HPC Biowulf cluster](https://hpc.nih.gov).
