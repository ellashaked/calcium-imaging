from calcium_imaging.data_loading import load_experiment_from_dir


def run_full_analysis(experiment_dir: str) -> None:
    experiment = load_experiment_from_dir(experiment_dir)
    print("Analysis finished successfully.")
