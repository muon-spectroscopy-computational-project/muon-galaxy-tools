import os
import sys
import yaml

def filefinder(root,substr,exception='',exceptfile=''):
    '''finds files with names containing substr
        within folder root and its subfolders'''
    filelst=[]
    for i in os.walk(root):
        for j in i[2]:
            #print(j)
            #pdb.set_trace()
            if substr in j and (exceptfile=='' or exceptfile not in j) and (exception=='' or exception not in i[0]):
                #print(j)
                filelst.append(i[0]+os.sep+j)
    return filelst

try:
    with open('params.yaml') as f:
        data=yaml.safe_load(f)
except FileNotFoundError:
    sys.stdout.write('default')
try:
    sys.stdout.write(data['out_folder'])
except KeyError:
    sys.stdout.write('default')
