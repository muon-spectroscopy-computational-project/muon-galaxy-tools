import argparse
import csv
from typing import List, Tuple

import matplotlib.pyplot as plt

X_AXIS_LABEL = "Energy (ev)"
Y_AXIS_LABEL = "Intensity"

column_names = ["Column 1", "Column 2"]


def create_tabular_file(x: List[float], y: List[float]) -> None:
    with open("plots/spectrum.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(column_names)
        for value1, value2 in zip(x, y):
            writer.writerow([value2, value1])


def create_plot_image(name: str, x: List[float], y: List[float]) -> None:
    plot_path = f"plots/{name}.png"
    plt.plot(x, y)
    plt.xlabel(X_AXIS_LABEL)
    plt.ylabel(Y_AXIS_LABEL)
    plt.savefig(plot_path)
    plt.close()


def read_file(data_file: str) -> Tuple[List[float], List[float]]:
    x: List[float] = []
    y: List[float] = []
    # read the data file
    with open(data_file, "r") as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            x.append(float(row[0]))
            y.append(float(row[1]))
    return x, y


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("-f", action="store_true")
    args = parser.parse_args()
    x, y = read_file(args.file_name)
    create_plot_image(args.file_name, x, y)
    if args.f:
        create_tabular_file(x, y)


if __name__ == "__main__":
    main()
