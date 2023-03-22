import json
import time

def find_keys_with_value(d, value, found_keys=None):
    if found_keys is None:
        found_keys = []
    for k, v in d.items():
        if isinstance(v, list):
            if value in v and k not in found_keys:
                found_keys.append(k)
                found_keys = find_keys_with_value(d, k, found_keys)
        elif isinstance(v, dict):
            found_keys = find_keys_with_value(v, value, found_keys)
    return found_keys

if __name__ == '__main__':
    start_time = time.time()
    with open('./temp/depth_1_dict.json') as json_file:
        dictionary = json.load(json_file)

    result = find_keys_with_value(dictionary, "tensorflow::Tensor::scalar")
    with open('./temp/top_function.txt', 'w') as f:
      #f.write(str(keep_namespace))
      f.write(str(result))

    end_time = time.time()
    print("time: ", end_time - start_time)
