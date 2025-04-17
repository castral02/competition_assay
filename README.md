Your README is clear, informative, and gives a solid walkthrough of the competition assay and AlphaPulldown workflow. With just a few tweaks for grammar, clarity, and consistency, it can read even more professionally while retaining its scientific and practical usefulness.

Here’s an edited version with comments folded into the improvements:

---

# Competition Assay

This repository contains Python code for a simple scoring method designed to identify highly interactive proteins using the AlphaPulldown pipeline.

## About

This code supports the findings in the paper **Hierarchical Small Molecule Inhibition of MYST Acetyltransferases** ([Chen et al., 2025]()). In our chemoproteomic experiments, we identified a new candidate member of the MYST KAT complexes: **FOXK2**. To explore FOXK2's potential role in these complexes, we developed a computational competitive assay for high-throughput discovery of protein-protein interactions.

## AlphaPulldown Workflow

We implemented the [AlphaPulldown Workflow](https://academic.oup.com/bioinformatics/article/39/1/btac749/6839971), and integrated the calculation of LIA and LIS scores, as described in the *Enhanced Protein-Protein Interaction Discovery via AlphaFold-Multimer* paper ([Kim et al., 2024](https://www.biorxiv.org/content/10.1101/2024.02.19.580970v1)).

We executed the AlphaPulldown workflow on the NIH HPC Biowulf Cluster. MSAs were generated via ColabFold, and AlphaPulldown 0.30.7 was used to compute mpDockQ/pDockQ scores.

➡️ To view folder structure examples, [click here](alphapulldown_materials/FOXK2_ex).

---

### How to Run on the Biowulf Cluster

#### **ColabFold Search**
```bash
sinteractive --mem=128g --cpus-per-task=16 --gres=lscratch:100
module load colabfold alphapulldown/0.30.7
colabfold_search --threads $SLURM_CPUS_PER_TASK for_colabfold.fasta $COLABFOLD_DB pulldown_cf_msas
create_individual_features.py --fasta_paths=bait.fasta,candidate.fasta --output_dir=pulldown_cf_msas \
    --use_precomputed_msas=True --max_template_date=2023-01-01 \
    --use_mmseqs2=True --skip_existing=True
```

#### **AlphaPulldown**
```bash
sinteractive --mem=150g -c8 --gres=lscratch:50,gpu:a100:1 --time=3-12:00:00
module load alphapulldown/0.30.7
run_multimer_jobs.py --mode=pulldown --num_cycle=3 --num_predictions_per_model=1 \
    --output_path=pulldown_model --protein_lists=candidate.txt,bait.txt \
    --monomer_objects_dir=pulldown_cf_msas

run_get_good_pae.sh --output_dir pulldown_model --cutoff=50
```

➡️ To view example `sbatch` files, [click here](alphapulldown_materials/sbatch_ex).

---

### How to Compute LIA/LIS Scores

We used the following [script](https://github.com/castral02/frag_af/blob/main/pipeline/lia_lis.py) to compute LIA and LIS values.

```bash
python3 lia_lis.py -output_dir=/path/to/AlphaPulldown/output/folders
```

➡️ Example [output file](alphapulldown_materials/alphapulldown_output.csv)

---

## Competition Assay

### Developing Metrics

Previous research has explored a multitude of AlphaFold-based metrics for understanding protein-protein interactions. Our goal was to develop a unified score incorporating multiple metrics, without bias toward a single one.

We focused on two key docking scores:
- [mpDockQ/pDockQ](https://www.nature.com/articles/s41467-022-33729-4)
- [LIA/LIS](https://www.biorxiv.org/content/10.1101/2024.02.19.580970v1)

We applied threshold-based filtering to these scores, and assigned a composite score based on the number of passed filters, with normalized summation.

➡️ Full workflow illustrated below:

### Workflow Diagram
![Workflow](images/scheme.png)

---

### How to Run

**Installation:**
```bash
git clone https://github.com/castral02/competition_assay
cd code
python3 competition_assay.py -csv_path=/path/to/csv/file -name=Protein
```

### Dependencies
```bash
absl-py
```

---

## Exploring Interface Contacts

To understand which residues are in contact between bait and candidate proteins, we developed two scripts compatible with AlphaFold2 and AlphaFold3 outputs.

### How to Run

**Installation:**
```bash
git clone https://github.com/castral02/competition_assay
cd code/interface_residues
python outputs.py -file /path/to/alphafold/summary/json/file  # For AF3
```

AlphaFold2 workflows require a `.pickle` file instead of JSON.

### Dependencies
```bash
json
pickle
biopython
scipy
```

---

## Declaration of Generative AI Usage

This project utilized OpenAI's ChatGPT to assist in generating Python code, documentation, and explanatory content.

---

## References

- Bryant, P., Pozzati, G., Zhu, W. et al. *Predicting the structure of large protein complexes using AlphaFold and Monte Carlo tree search*. **Nat Commun**, 13, 6028 (2022). [Paper Link](https://doi.org/10.1038/s41467-022-33729-4)

- Dingquan Yu, Grzegorz Chojnowski, Maria Rosenthal, Jan Kosinski. *AlphaPulldown—a Python package for protein–protein interaction screens using AlphaFold-Multimer*, **Bioinformatics**, 39(1), 2023. [Paper Link](https://doi.org/10.1093/bioinformatics/btac749)

- Kim AR, Hu Y, Comjean A, Rodiger J, Mohr SE, Perrimon N. *Enhanced Protein-Protein Interaction Discovery via AlphaFold-Multimer*. **bioRxiv** (2024). [Paper Link](https://www.biorxiv.org/content/10.1101/2024.02.19.580970v1)

> This work utilized the computational resources of the [NIH HPC Biowulf cluster](https://hpc.nih.gov).

---

Let me know if you'd like a badge section (e.g., Python version, license), a visual summary, or installation via `pip` or `conda` if applicable!
