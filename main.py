import argparse

from calcium_imaging import run_analysis


def main():
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment_dir", type=str, default="./raw_data/fish_NCLX_10-04-25")
    args = parser.parse_args()

    # analysis
    run_analysis(experiment_dir=args.experiment_dir)


if __name__ == '__main__':
    main()
