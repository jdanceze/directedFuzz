import os
import shutil

global i
i = 0
backed_up_files = []


def append_code_to_file(filename, target_line_number, code):
    global i

    with open(filename, 'r') as file:
        lines = file.readlines()

    lines.insert(target_line_number, code.format(I=i))

    with open(filename, 'w') as file:
        file.writelines(lines)
    i+=1

def append_header_to_file(filename, target_line_number, code):
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines.insert(target_line_number, code)
    with open(filename, 'w') as file:
        file.writelines(lines)


def increment_loc(list):
    for i in range(len(list)):
        list[i] = list[i] + (4 * i)
    return(list)
         

#filename = 'src/sub/list_kernels.h'
target_line_number = 897

target_lines = {
    'src/tensor.h': [916, 925],
    'src/sub/list_kernels.h': [897],
    './src/py_func.cc': [326, 186, 88]
}

code_chunk = '''
std::ofstream MyFile_{I}("/fileout/{I}.txt");
MyFile_{I} << "sth";
MyFile_{I}.close();
'''

header_chunk = '''
#include <iostream>
#include <fstream>
'''

for file in target_lines:
        print(file)
        if file not in backed_up_files:
            backed_up_files.append(file)
            bak_filename = file + '.bak'
            shutil.copyfile(file, bak_filename)

        target_line_list = target_lines.get(file)
        target_line_list.sort()
        print(target_line_list)
        increment_loc(target_line_list)
        for line_num in target_line_list:
            print(line_num)
            append_code_to_file(file, line_num, code_chunk)

for file in target_lines:
    append_header_to_file(file, 0, header_chunk)

with open('modified_file.txt', 'w') as f:
    for item in backed_up_files:
        f.write(str(item) + '\n')