import argparse

from pathlib import Path


def run_analysis(experiment_dir: str) -> None:
    experiment_dir_path = Path(experiment_dir)


def main():
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment_dir", type=str, default="./data/fish_NCLX_10-04-25")
    args = parser.parse_args()

    # analysis
    run_analysis(experiment_dir=args.experiment_dir)


if __name__ == '__main__':
    main()
