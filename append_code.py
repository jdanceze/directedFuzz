import os
import shutil

global i
i = 0
backed_up_files = []


def append_code_to_file(filename, target_line_number, code):
    global i

    with open(filename, 'r') as file:
        lines = file.readlines()
    print("target_line: ", lines[target_line_number])
    lines.insert(target_line_number, code.format(I=i))

    with open(filename, 'w') as file:
        file.writelines(lines)
    i+=1

def append_code_to_file_new(filename, target_line_number, code):
    global i

    with open(filename, 'r') as file:
        lines = file.readlines()

    #if target line not contain { then find the next line that contains { and insert code there
    if '{' not in lines[target_line_number]:
        print("target_line_number: ", target_line_number)
        print("target_line: ", lines[target_line_number])
        for line in lines[target_line_number:]:
            if '{' in line:
                target_line_number = lines.index(line)
                print("New target_line_number: ", target_line_number)
                break
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

def check_if_line_in_list(filename, line_list):
    new_line_list = []
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line_no in line_list:
        print("target_line_number: ", line_no)
        print("target_line: ", lines[line_no-1])
        if '{' not in lines[line_no-1]:
            print("not_target_line_number: ", line_no)
            print("not_target_line: ", lines[line_no-1])
            for line in lines[line_no:]:
                print("line: ", line)
                if '{' in line:
                    line_no = lines.index(line) + 1
                    new_line_list.append(line_no)
                    print("New_target_line_number: ", line_no)
                    print("New_target_line: ", lines[line_no])
                    break
        else:
            new_line_list.append(line_no)
    return new_line_list
        



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

# target_lines = {
#     'src/fractional_max_pool_op.cc': [71],
#     'src/fractional_pool_common.cc': [100, 20]
# }

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
        new_line_list = check_if_line_in_list(file, target_line_list)
        new_line_list.sort()
        print("new line list: ", new_line_list)
        increment_loc(new_line_list)
        for line_num in new_line_list:
            print(line_num)
            append_code_to_file(file, line_num, code_chunk)

# for file in target_lines:
#     append_header_to_file(file, 0, header_chunk)

with open('modified_file.txt', 'w') as f:
    for item in backed_up_files:
        f.write(str(item) + '\n')