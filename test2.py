import re

#with open('/Users/jdanceze/Desktop/hub/tensorflow/tensorflow/core/kernels/roll_op_new.cc', 'r') as f:
with open('/Users/jdanceze/Desktop/hub/tensorflow/tensorflow/core/kernels/image/generate_box_proposals_op.cu.cc', 'r') as f:
    file_contents = f.readlines()

function_name_to_search = "Roll"
combined_lines = ''.join([line.strip() for line in file_contents])
#remove all \ in the combined_lines
combined_lines = combined_lines.replace('\\', '')

# Use a regular expression to extract the function name and argument
#match = re.search(r'Name\("(.+?)"\).*?,\s*(\w+)', combined_lines)
matches = re.findall(r'Name\("(.+?)"\).*?,\s*(?:\w+::)?(\w+)', combined_lines)
for match in matches:
    #if match[0] == function_name_to_search:
    if True:
        print(f"Argument for function {function_name_to_search}: {match[1]}")
        #break

matche2 = re.search(r'Name\("(.+?)"\).*?,\s*(?:\w+::)?(\w+)', combined_lines)
if matche2:
    print(matche2.group(0))

    function_name = matche2.group(1)
    argument = matche2.group(2)
    print(f"Function name: {function_name}")
    print(f"Argument: {argument}")
else:
    print("No match found")


regex = r',\s*([\w:]+)'