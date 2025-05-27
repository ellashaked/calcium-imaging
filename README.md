# Calcium Imaging

Easily analyze VSI outputs.

## Getting Started

### 1. Installation

**Open [Google Colab](https://colab.research.google.com/)** and create a new notebook, for example `calcium-imaging.ipynb`.

**Install the toolkit** - execute this in the first cell of your notebook:

```shell
!rm -rf calcium-imaging && git clone https://github.com/ellashaked/calcium-imaging.git && cd calcium-imaging && pip install .
```

### 2. Setup Google Drive

**Link your personal Google Drive** - execute this in the second cell and click *Connect to Google Drive*:

```python
from google.colab import drive
from pathlib import Path

drive.mount('/drive', force_remount=True)
HOME = Path("/drive") / "MyDrive"
```

### 3. Path to raw data files

This toolkit scans your directory for `.xls` files named in the following format `<coverslip-id> - <group-type>.xls`.
Please make sure the files are in this format, otherwise you will encounter problems.

Add another cell in your notebook that holds that path to the directory (folder) with your VSI output files.

```python
experiment_dir = HOME / "path" / "to" / "fish_NCLX_10-04-25"
```

### 4. Reading experiments

To read an experiment, you first have to instantiate a `Preprocessor` object that will hold the preprocessing settings.

```python
from calcium_imaging import Preprocessor

preprocessor = Preprocessor(
    first_n_points_to_discard=5,
    smoothing_windows_size=2,
    normalization_sampling_start_frame=1,
    normalization_sampling_end_frame=35,
    earliest_onset_frame=50,
    earliest_baseline_recovery_frame=130,
    drop_traces_with_corrupted_peak=False,
    drop_time_col=True,
    drop_background_fluorescence_cols=True,
)
```

After you've set your preprocessor settings, you can load an experiment (multiple coverslips).

```python
from calcium_imaging import load_experiment

exp = load_experiment(
    experiment_dir=experiment_dir,
    preprocessor=preprocessor
)
```

### 5. Usage Examples

```python
exp["control"][3][15].visualize()  # experiment[<group>][<coverslip-id>][<roi-id>]
```

## API Reference

### `Experiment`

* `exp.save_mega_dfs(results_output_dir_path="./results")`
* `exp.visualize()` - Shows mean trace per group.
* `exp.visualize_all_rois()` - Shows the trace of every ROI in the experiment.
* `exp.visualize_eflux_bar_chart()` - Shows the eflux bar chart for all ROIs.
* `exp.visualize()`
* `exp.visualize()`