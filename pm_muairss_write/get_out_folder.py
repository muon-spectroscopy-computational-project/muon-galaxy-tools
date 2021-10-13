import sys

import yaml


try:
    with open('params.yaml') as f:
        data = yaml.safe_load(f)
except KeyError or FileNotFoundError:
    sys.stdout.write('muon-airss-out')
