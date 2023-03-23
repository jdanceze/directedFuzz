
with open('found_class.txt', 'r') as f:
    lines = f.readlines()

function_list = set()
for line in lines:
    parts = line.strip().split(',')
    filename = parts[0]
    function_name = parts[1]
    class_name = parts[2]
    
    #print(f"Filename: {filename}, Function name: {function_name}, Class name: {class_name}")
    function_list.add(function_name)

print("function binding found: ", len(function_list))


with open('not_found.txt', 'r') as f2:
    lines_2 = f2.readlines()
not_found_function_list = set()
for line in lines_2:
    #print(line)
    not_found_function_list.add(line)
print("function binding not found: ", len(not_found_function_list))