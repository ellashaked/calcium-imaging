import matplotlib.pyplot as plt
import pandas as pd

from calcium_imaging import load_experiment, Preprocessor, Experiment


def visualize_box_plot(df: pd.DataFrame, experiment_name: str) -> None:
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


def visualize_all_rois(experiment: Experiment) -> None:
    for group in experiment:
        for coverslip in group:
            for roi in coverslip:
                roi.visualize(title_prefix=f"{experiment.name} || {group}")


def main():
    preprocessor = Preprocessor(
        first_n_points_to_discard=5,
        smoothing_windows_size=2,
        normalization_sampling_start_frame=1,
        normalization_sampling_end_frame=35,
        earliest_onset_frame=50,
        earliest_baseline_recovery_frame=90,
        drop_traces_with_corrupted_peak=True,
        drop_time_col=True,
        drop_background_fluorescence_cols=True,
    )
    experiment = load_experiment(
        experiment_dir="./raw_data/fish_NCLX_long_and_short",
        preprocessor=preprocessor
    )
    # experiment.save_mega_dfs("./results")
    eflux_rates_df = pd.DataFrame.from_records(experiment.calculate_eflux_rates(return_json=True))
    visualize_box_plot(df=eflux_rates_df, experiment_name=experiment.name)
    # visualize_all_rois(experiment)

    print()


if __name__ == '__main__':
    main()
