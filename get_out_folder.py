import yaml
import sys
try:
    with open('params.yaml') as f:
        data=yaml.safe_load(f)
except:
    print('no param file')
    sys.stdout.write('default')
try:
    sys.stdout.write(data['out_folder'])
except Exception as e:
    print(e)
    sys.stdout.write('default')
