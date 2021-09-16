import yaml
import sys
import os
def filefinder(root,substr,exception='',exceptfile=''):
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
except:
    try:
        with open(filefinder('./','.yaml')[0]) as f:
            data=yaml.safe_load(f)
    except:
        print(filefinder('./','.yaml'))
        sys.stdout.write('default')
try:
    sys.stdout.write(data['out_folder'])
except Exception as e:
    sys.stdout.write('default')
