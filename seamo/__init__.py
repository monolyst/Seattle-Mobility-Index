import sys
import os
current = os.path.abspath(os.getcwd())
parent = current.find('seamo')
# print(current[:parent + len('scripts')] + '/')
sys.path.insert(0, current[:parent + len('seamo')])
DIRECTORIES = ['core', 'core/geocoder', 'analysis']
for directory in DIRECTORIES:
    path = os.path.join(current[:parent + len('seamo')] + '/', directory)
    # print(path)
    sys.path.insert(0, path)
