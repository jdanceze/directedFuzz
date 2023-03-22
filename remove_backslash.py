with open('./temp/depth_1_dict.json.bak') as file:
        contents = file.read()

contents = contents.replace('\\', '')

with open('./temp/depth_3_dict.json', 'w') as file:
    file.write(contents)