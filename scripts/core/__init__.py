import sys
import os
current = os.path.abspath(os.getcwd())
parent = current.find('scripts')
sys.path.insert(0, current[:parent + len('scripts')])