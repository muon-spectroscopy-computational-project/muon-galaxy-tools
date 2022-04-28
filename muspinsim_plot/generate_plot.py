import json
import sys

import matplotlib.pyplot as plt

import numpy as np


def main():
    input_json_path = sys.argv[1]

    plot_params = json.load(open(input_json_path, "r"))

    for series in plot_params["mu_out_series"]:
        mu_data = np.loadtxt(series['mu_data'], usecols=(0, 1))
        x, y = mu_data.T
        {
            'line': lambda x, y, label, c, args:
                plt.plot(x, y,
                         label=label,
                         c=c,
                         ls=args['linestyle'],
                         lw=args['linewidth']
                         ),
            'points': lambda x, y, label, c, args:
                plt.scatter(x, y,
                            label=label,
                            c=c,
                            s=args['pointscale'],
                            marker=args['pointstyle'],
                            )
        }.get(series['series_type']['type'])(
            x, y, series['mu_label'], series['colour'], series['series_type']
        )

    plt.xlabel(plot_params['xlab'])
    plt.ylabel(plot_params['ylab'])
    plt.title(plot_params['title'])
    plt.legend(loc="upper right")

    outfile = "outfile.{}".format(plot_params['out_file_type'])
    plt.savefig(outfile, format=plot_params['out_file_type'])


if __name__ == '__main__':
    main()
