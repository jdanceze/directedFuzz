import os

with open('./temp/modified_file.txt', 'r') as f:
    files = f.readlines()
    for file in files:
        print(file.strip())
        os.remove(file.strip())
        os.rename(file.strip() + '.bak', file.strip())