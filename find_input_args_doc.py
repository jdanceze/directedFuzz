import sys
from util import * 

    
def extract_function(file_path, function_name, output_file_path):
    with open(file_path) as f:
        lines = f.readlines()

    result = []
    result.append('import tensorflow as tf\n')
    for i in range(len(lines)):
        if function_name in lines[i]:
            for j in range(i, len(lines)):
                if "=" in lines[j]:
                    break
                result.append(lines[j])
            break
    result.append('=========\n')
    if len(result) > 2:
        with open(output_file_path, "w") as f:
        #with open(output_file_path, "a+") as f:
            f.write("".join(result))


if __name__ == '__main__':
    type_dict = {}
    #FUNC_NAME = "tf.raw_ops.MapStage"
    FUNC_NAME = sys.argv[1]
    print(FUNC_NAME)
    extract_function("./all_functions.txt", FUNC_NAME, "./one_func.txt")
