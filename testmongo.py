from pymongo import MongoClient
from pprint import pprint

client = MongoClient(
    "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
db = client.cloudeagle
collection = db.activeCompanies
links = []
# Issue the serverStatus command and print the results
for document in collection.find():
    if document.get('linkedin') is not None:
        links.append(document.get('linkedin')['value'])
    
print(len(links))
