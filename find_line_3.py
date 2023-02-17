import os
import glob
import re


# func_name = "CheckIsAlignedAndSingleElement"
# class_name = "Tensor"

# os.chdir('./src')
# cpp_files = glob.glob('*')

src_dir = './src'
cpp_files = []
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.cc') or file.endswith('.h'):
            cpp_files.append(os.path.join(root, file))

elements = ['tensorflow::PyFuncOp::Compute', 'tensorflow::anonymous_namespace\\{py_func::cc\\}::DoCallPyFunc', 'tensorflow::anonymous_namespace\\{py_func::cc\\}::MakeArgTuple']
scatter = ['tensorflow::TensorListScatter::Compute', 'tensorflow::Tensor::scalar', 'tensorflow::Tensor::CheckIsAlignedAndSingleElement']

for element in elements:
    element = re.sub(r'\\\{.*?\\\}', '', element)
    element = re.sub(r'\\\}.*?\\\{', '', element)
    parts = element.split('::')
    class_name = parts[1]
    func_name = parts[2]
    print(f"Second element: {class_name}, third element: {func_name}")

    for file in cpp_files:
        
        with open(file, 'r') as f:
            contents = f.read()
        #print("File: {}".format(file))
        found = False
        if func_name == "Compute":
            class_pattern = r'\b(class|struct|namespace)\s+' + class_name + r'\b'
        else:
            class_pattern = r'\b(class|struct|namespace)\s+' + class_name + r'\s*\{'
        
        class_check = re.search(class_pattern, contents)

        if class_check or func_name == "Compute":
            class_matches = re.finditer(class_pattern, contents)
        else:
            class_matches = None

        if class_matches is not None:
            for class_match in class_matches:
                #print("if")
                print("Class found in file {} on line {}: {}".format(file, contents.count('\n', 0, class_match.start()) + 1, class_match.group()))

                #function_pattern = r'\b' + func_name + r'\b\s*\([^)]*\)\s*(override)?\s*{'
                function_pattern = r'\b' + func_name + r'\b\s*\([^)]*\)\s*(?:const|\S*)\s*{'
                function_matches = re.finditer(function_pattern, contents[class_match.start():])

                for function_match in function_matches:
                    line_number = contents.count('\n', 0, class_match.start() + function_match.start()) + 1
                    print("  Function found in file {} on line {}: {}".format(file, line_number, function_match.group()))
                    found = True
                    if func_name == "Compute":
                        break
        else:
            #print("else")
            function_pattern = r'\b' + func_name + r'\b\s*\([^)]*\)\s*(?:const|\S*)\s*{'
            function_matches = re.finditer(function_pattern, contents)

            for function_match in function_matches:
                line_number = contents.count('\n', 0, function_match.start()) + 1
                print("  Function found in file {} on line {}: {}".format(file, line_number, function_match.group()))
        
        # if not found:
        #     print("if not found")
        #     function_pattern = r'\b' + func_name + r'\b\s*\([^)]*\)\s*(?:const|\S*)\s*{'
        #     function_matches = re.finditer(function_pattern, contents)

        #     for function_match in function_matches:
        #         line_number = contents.count('\n', 0, function_match.start()) + 1
        #         #print("not found")
        #         print("  Function found on line {}: {}".format(line_number, function_match.group()))
