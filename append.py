import os
import json
#combind all txt files in a directory into one txt file
def combine_txt_files(output_file):
    with open(output_file, 'w') as outfile:
        with open('list.json') as f:
            data = json.load(f)
            for i in data:
                print(i["TARGET_API_LIST"])
                with open(i["TARGET_API_LIST"]) as infile:
                    for line in infile:
                        outfile.write(line)

combine_txt_files("cve_list.txt")

