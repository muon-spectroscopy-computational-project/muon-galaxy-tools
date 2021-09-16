import sys
import os
import traceback
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

def replacedirs(text):
    spl=text.split('\n')
    for i in range(len(spl)):
        if spl[i][:10]=='chden_path':
            spl[i]=spl[i][:12]+'./'
    return '\n'.join(spl)

if __name__=='__main__':
    try:
        yamls=filefinder(sys.argv[1],'.yaml')
    except Exception as e:
        print('missing argument: root folder\n')
        traback.print_exc()
    for i in yamls:
        with open(i,'r') as f:
            x=f.read()
        out=replacedirs(x)
        with open(i,'w') as f:
            f.write(out)
        if i==yamls[-1]:
            with open(i,'r') as f:
                print(f.read())
    print('converted to relative path')
