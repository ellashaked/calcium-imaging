from calcium_imaging import load_experiment, Preprocessor


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
        experiment_dir="./raw_data/fish_NCLX_10-04-25",
        preprocessor=preprocessor
    )
    experiment.save_mega_dfs("./results")


if __name__ == '__main__':
    main()
