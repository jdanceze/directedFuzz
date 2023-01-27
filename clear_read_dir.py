import os
import json

with open('list.json') as f:
    data = json.load(f)
    for i in data:
        for file in os.listdir(i["READ_DIRECTORY"]):
            print("clearing READ_DIRECTORY: ", i["READ_DIRECTORY"] + "/" + file)
            os.remove(i["READ_DIRECTORY"]+ "/" + file)