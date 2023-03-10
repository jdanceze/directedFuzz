import os
import json

with open('list_valid.json') as f:
    data = json.load(f)
    for i in data:
        READ_DIRECTORY = i["READ_DIRECTORY"]
        FINAL_DIRECTORY_OUT = i["FINAL_DIRECTORY_OUT"]
        
        if not os.path.exists(READ_DIRECTORY):
            os.makedirs(READ_DIRECTORY)
        if not os.path.exists(FINAL_DIRECTORY_OUT):
            os.makedirs(FINAL_DIRECTORY_OUT)

        for file in os.listdir(i["FINAL_DIRECTORY_OUT"]):
            print("clearing FINAL_DIRECTORY_OUT: ", i["FINAL_DIRECTORY_OUT"] + "/" + file)
            os.remove(i["FINAL_DIRECTORY_OUT"]+ "/" + file)