import sys


toind = {'all': '0', 'uep': '1', 'dftb': '2', 'castep': '3'}
try:
    sys.stdout.write(toind[str(sys.argv[1])])
except FileNotFoundError:
    sys.stdout.write('default')
