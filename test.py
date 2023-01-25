import json

target = "tf.compat.v1.extract_volume_patches("
with open('list.json') as f:
    data = json.load(f)
    for i in data:
        print(i["READ_DIRECTORY"])
        if i["function"]+"(" == target: 
            print("Target api list: ", i["TARGET_API_LIST"])
    
    
    