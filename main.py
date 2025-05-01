import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from calcium_imaging import load_experiment, Preprocessor, Experiment


def visualize_eflux_box_plot(df: pd.DataFrame, experiment_name: str) -> None:
    plt.figure()
    plt.boxplot(
        [df.loc[df['group_type'] == g, 'eflux'] for g in df['group_type'].unique()],
        labels=df['group_type'].unique()
    )
    plt.xlabel('Group Type')
    plt.ylabel('Eflux Rate')
    plt.title(f'{experiment_name}\nDistribution of Eflux Rates by Group')
    plt.tight_layout()
    plt.show()


def visualize_amplitude_box_plot(df: pd.DataFrame, experiment_name: str) -> None:
    plt.figure()
    plt.boxplot(
        [df.loc[df['group_type'] == g, 'amplitude'] for g in df['group_type'].unique()],
        labels=df['group_type'].unique()
    )
    plt.xlabel('Group Type')
    plt.ylabel('Amplitude')
    plt.title(f'{experiment_name}\nDistribution of Amplitudes by Group')
    plt.tight_layout()
    plt.show()


def visualize_all_rois(experiment: Experiment) -> None:
    for group in experiment:
        for coverslip in group:
            for roi in coverslip:
                roi.visualize(title_prefix=f"{experiment.name} || {group}")


def main():
    raw_data_dir = "./raw_data"
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
    for experiment_dir in Path(raw_data_dir).iterdir():
        if not experiment_dir.is_dir():
            continue
        print("-" * 50)
        print(experiment_dir.stem)
        print("-" * 50)
        experiment = load_experiment(experiment_dir=experiment_dir, preprocessor=preprocessor)
        experiment["control"][8][4].set_peak_idx(5)
        experiment["control"][8][4].visualize()
        # experiment.save_mega_dfs("./results")
        # eflux_rates_df = pd.DataFrame.from_records(experiment.calculate_eflux_rates(return_json=True))
        # visualize_eflux_box_plot(df=eflux_rates_df, experiment_name=experiment.name)
        #
        # amplitudes_df = pd.DataFrame.from_records(experiment.calculate_amplitudes(return_json=True))
        # visualize_amplitude_box_plot(df=amplitudes_df, experiment_name=experiment.name)

        visualize_all_rois(experiment)

    print()


if __name__ == '__main__':
    main()
