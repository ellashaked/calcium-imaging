from pathlib import Path

from calcium_imaging.instantiation import load_experiment_from_dir


def build_mega_dfs(experiment_dir: str, results_output_dir_path: str = "./results") -> None:
    experiment = load_experiment_from_dir(experiment_dir)
    results_output_dir_path = Path(results_output_dir_path) / Path(experiment_dir).stem
    results_output_dir_path.mkdir(parents=True, exist_ok=True)
    for experimental_condition, df in experiment.experimental_condition_to_df.items():
        base = results_output_dir_path / experimental_condition
        df.to_excel(base.with_suffix(".xlsx"), index=False)
        df.to_csv(base.with_suffix(".csv"), index=False)
    print(f"Successfully saved {experiment.num_experimental_conditions} mega dfs to "
          f"{results_output_dir_path.resolve()}")
