import subprocess
from pymongo import MongoClient
from pprint import pprint
import sys

client = MongoClient(
    "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
db = client.cloudeagle
collection = db.activeCompanies
links = []
# Issue the serverStatus command and print the results
count = collection.count()
split_count = int(count/int(sys.argv[1]))
for i in range(int(sys.argv[1])):
    print(split_count*i, split_count)
    try:
        popen = subprocess.Popen("python test.py {0} {1}".format(split_count*i + 1, split_count), stdout=subprocess.PIPE, shell=True, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            print(stdout_line) 
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, "python test.py {0} {1}".format(split_count*i, split_count))
    except:
        print('Error for:',"python test.py {0} {1}".format(split_count*i, split_count))
