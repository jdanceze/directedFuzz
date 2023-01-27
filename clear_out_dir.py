import os
import json

with open('list.json') as f:
    data = json.load(f)
    for i in data:
        
        for file in os.listdir(i["FINAL_DIRECTORY_OUT"]):
            print("clearing FINAL_DIRECTORY_OUT: ", i["FINAL_DIRECTORY_OUT"] + "/" + file)
            os.remove(i["FINAL_DIRECTORY_OUT"]+ "/" + file)