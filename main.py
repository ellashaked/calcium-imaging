import argparse

from calcium_imaging import load_experiment_from_dir


def main():
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment_dir", type=str, default="./raw_data/fish_NCLX_10-04-25")
    args = parser.parse_args()

    # run
    experiment = load_experiment_from_dir(experiment_dir=args.experiment_dir)
    dfs = experiment.get_group_type_to_df()
    print()


if __name__ == '__main__':
    main()
