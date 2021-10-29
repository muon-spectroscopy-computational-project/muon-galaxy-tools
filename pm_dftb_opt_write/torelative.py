import os
import sys
import traceback


def filefinder(root, substr, exception='', exceptfile=''):
    '''find files with names containing substr
        within folder root '''
    filelst = []
    for i in os.walk(root):
        for j in i[2]:
            if (substr in j and (exceptfile == '' or exceptfile not in j) and
                    (exception == '' or exception not in i[0])):
                filelst.append(i[0]+os.sep+j)
    return filelst


def replacedirs(text):
    '''replace chden_path in subfolders with cwd'''
    spl = text.split('\n')
    for i in range(len(spl)):
        if spl[i][:10] == 'chden_path':
            spl[i] = spl[i][:12]+'./'
    return '\n'.join(spl)


if __name__ == '__main__':
    try:
        yamls = filefinder(sys.argv[1], '.yaml')
    except FileNotFoundError:
        print('missing argument: root folder\n')
        traceback.print_exc()
    for yamlfile in yamls:
        with open(yamlfile, 'r') as f:
            x = f.read()
        replaced = replacedirs(x)
        with open(yamlfile, 'w') as f:
            f.write(replaced)
        if yamlfile == yamls[-1]:
            with open(yamlfile, 'r') as f:
                print(f.read())
    print('converted to relative path')
