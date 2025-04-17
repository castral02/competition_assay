# Competition Assay

This repository contains Python code for a computational competition assay that integrates AlphaPulldown-derived scores to rank candidate interactors based on predicted binding quality.

## About

This code supports the findings in the paper ___________. In our chemoproteomic experiments, we identified a new candidate member of the MYST KAT complexes: **FOXK2**. To explore FOXK2's potential role in these complexes, we developed a computational competitive assay for high-throughput discovery of protein-protein interactions.

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

The input CSV must contain the following columns:
- `average lia score`
- `lis_score`
- `mpDockQ/pDockQ`

These are computed using AlphaPulldown and the `lia_lis.py` script from [frag_af](https://github.com/castral02/frag_af).

```bash
python3 lia_lis.py -output_dir=/path/to/AlphaPulldown/output/folders
```

➡️ Example [output file](alphapulldown_materials/alphapulldown_output.csv)

---

## Competition Assay

### Developing Metrics

Previous research has explored a multitude of AlphaFold-based metrics for understanding protein-protein interactions. Our goal was to develop a unified interaction score that integrates multiple structural metrics, normalized and weighted to reduce bias toward any single predictor.

We focused on two key docking scores:
- [mpDockQ/pDockQ](https://www.nature.com/articles/s41467-022-33729-4)
- [LIA/LIS](https://www.biorxiv.org/content/10.1101/2024.02.19.580970v1)

We applied threshold-based filtering to LIA, LIS, and mpDockQ scores. A composite score was then calculated by scaling a normalized sum of these metrics according to the number of filters passed, emphasizing high-confidence interactions.

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
pandas
```

The [output CSV](examples/output_competition_assay_ex.csv) contains:
- Original input columns
- Normalized values for each metric
- Composite_Score
- Rank

Example:
| Job     |...| mpDockQ/pDockQ| lis_score | ... | Composite_Score  | Rank |
|---------|---|---------------|-----------|-----|------------------|------|
| FOXK2   |...|0.74           | 0.12      | ... | 2.45             | 1    |

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

➡️ Example [AF3 output file](examples/wdr5_foxk2_human_af3_ex.csv)

➡️ Example [AF2 output file](examples/wdr5_foxk2_human_af2_ex.csv)

### Dependencies
```bash
json
pickle
biopython
scipy
pandas
absl-py
numpy
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
