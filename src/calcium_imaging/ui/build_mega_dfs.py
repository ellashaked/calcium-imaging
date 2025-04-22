from pathlib import Path

from calcium_imaging.data_loading import load_experiment_from_dir


def build_mega_dfs(experiment_dir: str, results_output_dir_path: str = "./results") -> None:
    experiment = load_experiment_from_dir(experiment_dir)
    results_output_dir_path = Path(results_output_dir_path) / Path(experiment_dir).stem
    for experimental_condition, df in experiment.experimental_condition_to_df.items():
        df.to_excel(results_output_dir_path / f"{experimental_condition}.xlsx")
    print(f"Successfully saved {len(experiment.num_experimental_conditions)} mega dfs to "
          f"{results_output_dir_path.resolve()}")
