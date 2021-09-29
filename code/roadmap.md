## Roadmap
A description of how this dataset was curated and an explanation of the code in this directory.

### Collected T1 data, metadata (e.g. age,sex)
Normative T1 data were collected from several labs at the University of Pennsylvania. The data were identified on Flywheel and added to a 'Collection' which can be found [here](https://upenn.flywheel.io/#/collections/5eb5081448fe1b1e5792a7a9).
The original excel files sent to me listing subjects can be found in `data_collection/originals`. Edited versions of these files `*metadata.csv`, as well as notes about the data collection process `accounting_notes` and a summary of the dataset `accounting_summary.csv`, can be found at the top level of the `data_collection` directory. 

`import_ftdc.ipynb` was used to cross-reference the FTDC spreadsheet with the data on Flywheel to ensure the correct data were being added to the collection.
`accounting.ipynb` keeps track of what is in the Flywheel collection and generates the statistics and plots summarizing the dataset.
`id_missing_scans.ipynb` was used to track discrepancies in the local spreadsheet (`metadata.csv`) and the Flywheel collection.

### QC'd T1 data
QC evaluations, which can be found in healthy-t1-dataset/metadata.csv, follow these critera:
  3 - perfect
  2 - usable
  1 - unusable
  
  and are scored for the presence of motion and artifact (1 meaning present and 0 meaning not present).
  Examples of artifacts are included in the `qc/` directory.

### Ran ANTs Cortical thickness and download results
The outcome metric we are interested in for the purposes of the Neuroprint gear is cortical thickness. The ANTs-CT Flywheel Gear was run on the normative dataset using `run_antsct.ipynb`. Note that this ran the **antsct-fw** gear, not **antsct-aging-fw** gear so results were not automatically projected to the Schaefer atlas. 

### Projected Schaefer atlas labels to subjects' space
For the regional analysis, the cortical thickness metrics needed to be in the same space as the Schaefer atlas (MNI). Some necessary warp files were already created by ANTs Cortical Thickness, including the cortical mask, the extracted brain, generic affine and warp for mapping subject to template and vice versa. These files were downloaded from each subject with `download_warps.ipynb` and the transform was applied using `scripts/propagateToNative.sh` Double check that all files were downloaded with `check_completion.ipynb`

### Calculated mean CT in every label for every control subject
Extracted cortical thickness statistics from each label (e.g. mean, median, min, max, 1Q, 3Q).
Created a csv for *each* subject, e.g.`test_sub/118785/sub-118785_schaefer.csv`.

### Ran separate linear regression for each label
Took the csvs from the previous step and plugged the data into a linear model with `scripts/calc_coeffs.py`. The result is the list of coefficients for each label, e.g. `ws_coeffs_07-19-2021.csv`, the diamond of this whole pipeline.
