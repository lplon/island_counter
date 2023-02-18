import argparse
from island_map import IslandMap


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")

    args = parser.parse_args()

    island_map = IslandMap(args.path)
    island_map.find_islands()

    print(island_map.island_count)