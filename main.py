import matplotlib.pyplot as plt
import pandas as pd

from calcium_imaging import load_experiment, Preprocessor


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


def main():
    preprocessor = Preprocessor(
        first_n_points_to_discard=5,
        smoothing_windows_size=2,
        normalization_sampling_start_frame=1,
        normalization_sampling_end_frame=35,
        drop_time_col=True,
        drop_background_fluorescence_cols=True,
    )
    experiment = load_experiment(
        experiment_dir="./raw_data/SI_SH_check",
        preprocessor=preprocessor
    )
    # experiment.save_mega_dfs("./results")
    eflux_rates_df = pd.DataFrame.from_records(experiment.calculate_eflux_rates(return_json=True))
    visualize_box_plot(df=eflux_rates_df, experiment_name=experiment.name)
    for group in experiment:
        for coverslip in group:
            for roi in coverslip:
                roi.visualize(title_prefix=f"{experiment.name} || {group}")
    print()


if __name__ == '__main__':
    main()
