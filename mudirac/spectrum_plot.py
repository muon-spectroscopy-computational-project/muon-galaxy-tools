import sys
import csv
import matplotlib.pyplot as plt
from typing import List

X_AXIS_LABEL = "Energy (ev)"
Y_AXIS_LABEL = "Intensity"

def main(data_file: str) -> None:
    x: List[float] = []
    y: List[float] = []
    plot_path = f"plots/{data_file}.png"
    #read the data file
    with open(data_file,'r') as file:
        reader =  csv.reader(file,delimiter='\t')
        for row in reader:
            x.append(float(row[0]))
            y.append(float(row[1]))
    plt.plot(x,y)
    plt.xlabel(X_AXIS_LABEL)
    plt.ylabel(Y_AXIS_LABEL)
    plt.savefig(plot_path)
    plt.close()

if __name__ == '__main__':
    spectrum_file: str = sys.argv[1]
    main(spectrum_file)