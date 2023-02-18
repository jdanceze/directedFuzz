import os
import glob
import re


src_dir = './src'
cpp_files = []
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.cc') or file.endswith('.h'):
            cpp_files.append(os.path.join(root, file))

with open('found_class.txt', 'r') as f:
    lines = f.readlines()
global i
i=0
for line in lines:
    parts = line.strip().split(',')
    filename = parts[0]
    function_name = parts[1]
    class_name = parts[2]
    #print(f"Filename: {filename}, Function name: {function_name}, Class name: {class_name}")

    with open(filename, 'r') as f:
        contents = f.read()
        print("File: " + filename)
        print("Class name: " + class_name)
        found = False
        class_pattern = r'\b(class|struct|namespace)\s+' + class_name
        print("Class pattern: " + class_pattern)
        class_check = re.search(class_pattern, contents)

        if class_check:
            #print("Found class")
            class_matches = re.finditer(class_pattern, contents)
        else:
            class_matches = None

        if class_matches is not None:
            print("Found class")
            i+=1
        else:
            with open('class_not_found.txt', 'a') as f:
                f.write(f"{filename},{class_name}\n")
print(i)

