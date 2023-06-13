import json
import sys

import numpy as np

import scipy.stats as stats


def main():
    input_json_path = sys.argv[1]
    params = json.load(open(input_json_path, "r"))

    x_equal = True
    data = np.loadtxt(params["data_in"][0], usecols=(0, 1))
    x_values = [data[:, 0]]
    y_values = [data[:, 1]]
    bins = len(data)

    for path in params["data_in"][1:]:
        data = np.loadtxt(path, usecols=(0, 1))
        x_values.append(data[:, 0])
        y_values.append(data[:, 1])
        length_equal = bins == len(data)
        bins = min(bins, len(data))
        x_equal = (
            x_equal and length_equal and np.allclose(x_values, x_values[-1])
        )

    if x_equal:
        print(
            "All x ranges were identical, performing direct average over "
            f"{len(x_values)} files"
        )
        means = np.mean(y_values, axis=0)
        np.savetxt("data_out.dat", np.column_stack((x_values[0], means)))
        return

    if params["bins"] is not None:
        bins = params["bins"]

    x_flat = np.concatenate(x_values)
    y_flat = np.concatenate(y_values)
    print(f"Averaging {len(x_flat)} data points into {bins} bins")
    means, edges, _ = stats.binned_statistic(x_flat, y_flat, bins=bins)
    data_out = np.column_stack(((edges[1:] + edges[:-1]) / 2, means))
    np.savetxt("data_out.dat", data_out)


if __name__ == "__main__":
    main()
