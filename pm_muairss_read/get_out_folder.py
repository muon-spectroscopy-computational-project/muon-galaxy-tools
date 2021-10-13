import os
import sys

import yaml


try:
    with open('params.yaml') as f:
        data = yaml.safe_load(f)
        sys.stdout.write(data['out_folder'])
except FileNotFoundError or KeyError:
    sys.stdout.write('muon-airss-out')
