import os
import re

function_interface = "tf.raw_ops.UnsortedSegmentProd"
function_interface = function_interface.split('.', 1)[1]
#print(function_interface)
function_interface = "tf_export(" + '"' + function_interface + '"' + ")"
print("Finding: ", function_interface)

gen_path = "/opt/homebrew/Caskroom/miniforge/base/lib/python3.10/site-packages/tensorflow/python/"
src_path = "/Users/jdanceze/Desktop/hub/tensorflow/"
target_file = None
target_register_op = None
target_class = False

def get_alphanumeric(string):
    result = ''
    for char in string:
        if char.isalnum():
            result += char
    return result


for root, dirs, files in os.walk(gen_path):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                for line_number, line in enumerate(f):
                    if function_interface in line:

                        if "gen_" not in file:
                            print("This is not gen file")
                            print("Skipping: ", file)
                        else:
                            print("================Regis=====================")
                            print("Found: ", function_interface)
                            print("File Path: ", file_path)
                            print("File: ", file)
                            print("Line number: ", line_number + 1)
                            print("Line: ", line)
                            target_register_op = line.split('=')[0].strip()
                            print("Target: ", target_register_op)
                            break
                        #print(f"File: {file_path}, Line {line_number + 1}: {line}")

# if target_register_op is not None:
#     target_register_op_Name = "Name(" + '"' + target_register_op + '"' + ")"
#     for root, dirs, files in os.walk(src_path):
#         for file in files:
#             if file.endswith('.cc') or file.endswith('.h'):
#                 file_path = os.path.join(root, file)
#                 with open(file_path, 'r') as f:
#                     for line_number, line in enumerate(f):
#                         if target_register_op_Name in line:
#                             print("\nFound: ", target_register_op_Name)
#                             print("File Path: ", file_path)
#                             print("File: ", file)
#                             print("Line number: ", line_number + 1)
#                             print("Line: ", line)
#                             target_file = file_path
#                             # last_value = line.split()[-1].strip(';')
#                             # last_value = last_value[:-1]
#                             #print(last_value)

#                             match = re.search(r',\s*(\w+)\);', line)
#                             if match:
#                                 var_name = match.group(1)
#                                 print(f"Argument : {var_name}")
#                                 print("==============File=============")
#                             else:
#                                 print("No match found.")
#                                 print("try again")
#                                 #next_line = next(f)
#                                 # print("Next line: ", next_line)
#                                 # end = next_line.find("<")
#                                 # value = next_line[:end]
#                                 # print(get_alphanumeric(value))
#                                 # print("=====================================")
#                                 with open(file_path, 'r') as f:
#                                     file_contents = f.readlines()

#                                 function_name_to_search = target_register_op
#                                 combined_lines = ''.join([line.strip() for line in file_contents])
#                                 #remove all \ in the combined_lines
#                                 combined_lines = combined_lines.replace('\\', '')
#                                 matches = re.findall(r'Name\("(.+?)"\).*?,\s*(?:\w+::)?(\w+)', combined_lines)
#                                 for match in matches:
#                                     if match[0] == function_name_to_search:
#                                         print(f"Argument for function {function_name_to_search}: {match[1]}")
#                                         print("==============File=============")
#                                         break



if target_register_op is not None:
    target_register_op_Name = "Name(" + '"' + target_register_op + '"' + ")"
    for root, dirs, files in os.walk(src_path):
        for file in files:
            if file.endswith('.cc') or file.endswith('.h'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    file_contents = f.readlines()
                    function_name_to_search = target_register_op
                    combined_lines = ''.join([line.strip() for line in file_contents])
                    combined_lines = combined_lines.replace('\\', '')
                    matches = re.findall(r'Name\("(.+?)"\).*?,\s*(?:\w+::)?(\w+)', combined_lines)
                    for match in matches:
                        if match[0] == function_name_to_search:
                            target_class = True
                            print("==============Class=============")
                            print("Found: ", target_register_op_Name)
                            print("File Path: ", file_path)
                            print("File: ", file)
                            #print("Line number: ", line_number + 1)
                            #print("Line: ", line)
                            print(f"\nArgument for function {function_name_to_search}: {match[1]}")
                            break

