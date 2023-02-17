import os
import glob
import re

# define the function or class name to search for
func_name = "Compute"
class_name = "TensorListPopBack"
# navigate to the directory containing your C++ source code
os.chdir('./src')

# find all C++ source code files in the directory
cpp_files = glob.glob('list_kernels.h')

# iterate through each C++ source code file
for file in cpp_files:
    # read in the contents of the file as a string
    with open(file, 'r') as f:
        contents = f.read()

    # use regular expressions to search for the class name in the string
    class_pattern = r'\b(class|struct|namespace)\s+' + class_name + r'\b'
    class_matches = re.finditer(class_pattern, contents)

    # iterate through each match for the class
    for class_match in class_matches:
        print("Class found in file {} on line {}:".format(file, contents.count('\n', 0, class_match.start()) + 1))
        print(class_match.start())
        print(class_match.end())
        # search for the function within the class
        function_pattern = r'\b' + func_name + r'\b\s*\('
        function_matches = re.finditer(function_pattern, contents[class_match.end():])

        # iterate through each match for the function within the class
        for function_match in function_matches:
            line_number = contents.count('\n', 0, class_match.start() + function_match.start()) + 1
            print("  Function found on line {}: {}".format(line_number, function_match.group()))
