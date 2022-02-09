import sys
import importlib

try:
    mod = importlib.import_module(sys.argv[1])
    config = []
    if sys.argv[2] == 'easy':
        config = mod.easy
    if sys.argv[2] == 'medium':
        config = mod.medium
    if sys.argv[2] == 'hard':
        config = mod.hard
    if sys.argv[2] not in ['easy', 'medium' ,'hard']:
        raise
except Exception as exception: 
    print ("Number of arguments: ", len(sys.argv))
    print ("The arguments are: " , str(sys.argv))
    print("---You need to pass three arguments: /config file name/ /difficulty (easy, medium or hard)/ /number of scenarios to generate/---")
    raise

print("easy nPumps: " , config['pumpFailN'])