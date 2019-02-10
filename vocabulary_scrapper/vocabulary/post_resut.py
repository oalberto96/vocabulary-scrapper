import json

def read_result():
    with open('result.json') as file:
        data = json.load(file)
    return data


username
