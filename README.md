# FTIR Spectral Image Classification — Data Curation and ML Development

**Author:** Alejandro Javier Alegre Reyes  
**Status:** Dataset inventory and reproducibility audit; ML performance **not yet validated**.

## Objective
Develop reproducible machine-learning approaches to recognize chemical functional groups from FTIR spectral images, with attention to multi-label chemical structures and scientifically defensible evaluation.

## Dataset
The current inventory contains **498 FTIR PNG records** curated from SDBS-sourced material: **140 alcohol**, **162 amine**, and **196 ketone** folder entries. These are original collection categories, **not yet validated multi-label ground truth**. Source: SDBS (AIST), https://sdbs.db.aist.go.jp/.

The image files are not included in this starter repository. The inventoried filenames and file checksums are documented in `data/inventory_498.csv`. Local Google Drive paths were removed from the published inventory.

## Data quality and limitations
- **463/498** structure records remain flagged `PENDENTE`, with **35** linked by name; name-based links require independent structural review.
- Historical partitions: **306** train, **71** test, **71** validation, **50** excluded pending review. They are **not approved as final ML splits**.
- **123 repeated compound identifiers** beyond the first instance (the count is repeated records, not necessarily 123 distinct compounds). No duplicate SHA-256 hashes were recorded in the inventory.
- Multiple functional groups may coexist in one molecule; folder-based 3-class labels must not be treated as validated ground truth.
- Compound-grouped splitting and multi-label verification are necessary before reporting model results to prevent data leakage.

## Run the audit
```bash
python -m pip install -r requirements.txt
python scripts/audit_inventory.py
```
The audit summarizes the dataset and counts compounds occurring across historical train/validation/test partitions.

## Planned modeling (not yet completed or validated)
1. Confirm molecule identities and chemically correct multi-label targets.
2. Resolve duplicate/near-duplicate compounds and construct group-based train/validation/test splits.
3. Benchmark HOG + SVM and CNN image classification baselines.
4. Evaluate per-label precision/recall/F1, macro/micro F1, confusion/error patterns and reproducibility.
5. Publish training scripts, exact dependencies, seeds, model cards, and representative tests after validation.

## Data permission and provenance
The project owner reports receiving SDBS authorization. **Verify the written permission's exact scope** (redistribution of spectral PNGs, derivative datasets, public GitHub hosting, and attribution requirements) before uploading image files. This starter package does not include the original spectral images or the authorization letter.

## License
No public license is assigned to the underlying spectra. Repository source code may be licensed separately once approved; a blanket license must not imply ownership of SDBS records.

## Next stage: label audit and executable baseline
The author has reported SDBS authorization; the exact redistribution conditions should be retained with the repository before publishing spectral images.

`data/labels_to_review.csv` is a **review template**, not ground truth. All multi-label entries intentionally start blank. `familia_original` is a legacy storage category, not a verified label. A domain reviewer should populate `verified_compound_id` and `label_alcohol`, `label_amine`, `label_ketone` with **0** or **1** after structural review. Different images of the same compound must share the same verified compound ID.

Run locally, or in Google Colab after mounting Drive and setting a folder containing the PNG images:

```bash
pip install -r requirements.txt
python scripts/audit_inventory.py
python scripts/check_dataset.py --images '/content/drive/MyDrive/FTIR_images'
python scripts/train_baseline.py --images '/content/drive/MyDrive/FTIR_images'
```

The training baseline **will not run** on the unreviewed inventory. Once validated, it uses grayscale resizing (256×128), HOG features, independent one-versus-rest logistic models for each chemical group, and a compound-grouped random holdout. It reports F1 scores only from real execution. This baseline is not a CNN and does not claim any existing accuracy. Baseline limitations: image layouts may introduce artifacts; a single holdout is not a substitute for external testing; multi-label reviews must be chemically justified.

Avoid uploading full image archives or authorization correspondence until their publication terms and personal information are checked.
