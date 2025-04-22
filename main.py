import argparse

from calcium_imaging.ui import build_mega_dfs


def main():
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment_dir", type=str, default="./raw_data/fish_NCLX_10-04-25")
    args = parser.parse_args()

    # run
    build_mega_dfs(experiment_dir=args.experiment_dir)


if __name__ == '__main__':
    main()
