from pymongo import MongoClient
from bson.json_util import dumps
from copy import deepcopy
import pandas
import json

def connect_to_db():
    client = MongoClient(
        "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
    db = client.cloudeagle
    return db

db = connect_to_db()
activeCompanies = db.activeCompanies
stackData = db.stackData

catdict = {}
json = db.test5.find()


with open('products.json', 'w') as file:
    file.write('[')
    for document in json:
        file.write(dumps(document))
        file.write(',')
    file.write(']')

def cross_join(left, right):
    new_rows = [] if right else left
    for left_row in left:
        for right_row in right:
            temp_row = deepcopy(left_row)
            for key, value in right_row.items():
                temp_row[key] = value
            new_rows.append(deepcopy(temp_row))
    return new_rows


def flatten_list(data):
    for elem in data:
        if isinstance(elem, list):
            yield from flatten_list(elem)
        else:
            yield elem


def json_to_dataframe(data_in):
    def flatten_json(data, prev_heading=''):
        if isinstance(data, dict):
            rows = [{}]
            for key, value in data.items():
                rows = cross_join(rows, flatten_json(value, prev_heading + '.' + key))
        elif isinstance(data, list):
            rows = []
            for i in range(len(data)):
                [rows.append(elem) for elem in flatten_list(flatten_json(data[i], prev_heading))]
        else:
            rows = [{prev_heading[1:]: data}]
        return rows

    return pandas.DataFrame(flatten_json(data_in))

print(json)
df = json_to_dataframe(json)
print(df[:10])

