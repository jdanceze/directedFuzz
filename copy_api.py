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
    result.append('=========')
    with open(output_file_path, "w") as f:
        f.write("".join(result))

extract_function("./all_functions.txt", "tf.data.experimental.make_batched_features_dataset", "./one_func.txt")
