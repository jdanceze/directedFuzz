import os

function_interface = "tf.raw_ops.PyFunc"
function_interface = function_interface.split('.', 1)[1]
#print(function_interface)
function_interface = "tf_export(" + '"' + function_interface + '"' + ")"
print("Finding: ", function_interface)

gen_path = "/opt/homebrew/Caskroom/miniforge/base/lib/python3.10/site-packages/tensorflow/python/"
src_path = "/Users/jdanceze/Desktop/hub/tensorflow/"
target_file = None

for root, dirs, files in os.walk(gen_path):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                for line_number, line in enumerate(f):
                    if function_interface in line:
                        print("\nFound: ", function_interface)
                        print("File Path: ", file_path)
                        print("File: ", file)
                        print("Line number: ", line_number + 1)
                        print("Line: ", line)
                        target_register_op = line.split('=')[0].strip()
                        print("Target: ", target_register_op)
                        #print(f"File: {file_path}, Line {line_number + 1}: {line}")
