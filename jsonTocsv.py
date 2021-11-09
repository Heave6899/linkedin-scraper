from copy import deepcopy
import pandas
import json

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

with open("productcat2.json", "r+") as f:
    data = (''.join(f.readlines())).replace('\n','')

# print(data)
data = json.loads(data)
df = json_to_dataframe(data)
print(df)

df.to_excel("products3.xlsx", columns=["_id.company_size", '_id.product_category', '_id.product_name', 'count'],  header=['Company Size', 'Category','Product Name', 'Count'], index=False)

