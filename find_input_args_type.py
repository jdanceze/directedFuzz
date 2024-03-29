import sys
import tensorflow as tf
import inspect

from util import * 

dtype_anno = 'D_TYPE'
ds_anno = 'D_STRUCTURE'
anno_dict = [
    #{'dtype': dtype_anno},
    {'structure': ds_anno},
    #{'tensor_t': ds_anno}
]


pre_normalize ={
    r'floating point': 'float',
    r'floating-point': 'float',
    r'A list of `Tensor`': 'tensor',
    r'`Tensor`': 'tensor',
    # r'data\s+type': 'dtype',

}

type_map = {
    'list' : ('list', 'tuple', 'ndarray'),
    'lists' : ('list', 'tuple', 'ndarray'),
    'tuple' : ('list', 'tuple', 'ndarray'),
    'int' : ('int', 'int8', 'int16', 'int32', 'int64'),
    'string' : ('str', 'bytes', 'bytes_'),
    'bool' : ('bool', 'bool_'),
    'dict' : ('dict'),
    'dictionary' : ('dict'),
    'sparsetensor': ('Tensor','EagerTensor','Literal', 'RaggedTensor', 'RaggedTensorDynamicShape', 'RaggedTensorValue', 'range', 'SparseTensor','list', 'tuple', 'ndarray','int', 'int8', 'int16', 'int32', 'int64', 'str', 'bytes', 'bytes_'),
    'tensors': ('Tensor','EagerTensor','Literal', 'RaggedTensor', 'RaggedTensorDynamicShape', 'RaggedTensorValue', 'range', 'SparseTensor','list', 'tuple', 'ndarray','int', 'int8', 'int16', 'int32', 'int64', 'str', 'bytes', 'bytes_'),
    'tensor': ('Tensor','EagerTensor','Literal', 'RaggedTensor', 'RaggedTensorDynamicShape', 'RaggedTensorValue', 'range', 'SparseTensor','list', 'tuple', 'ndarray','int', 'int8', 'int16', 'int32', 'int64', 'str', 'bytes', 'bytes_'),
}

def sub_kw(src_text, framework):
    anno_map = {dtype_anno: [], ds_anno:[]}

    normalized_text = src_text
    dtype_ls = read_yaml('./dtype_ls_tf.yaml')[framework]

    for anls in anno_dict:
        category = next(iter(anls))
        keywords = dtype_ls[category]
        keywords = sorted(keywords, key=len, reverse=True)
        p = get_bigrex(sorted(keywords, key=len, reverse=True), boundary=True, escape=True)
        p = r'`*({})`*'.format(p)
        anno_map[anls[category]] += re.findall(p, normalized_text, flags=re.IGNORECASE)
        if len(anno_map[anls[category]]) == 0:
            continue
        return anno_map[anls[category]][0]
    
def extract_function(file_path, function_name, output_file_path):
    with open(file_path) as f:
        lines = f.readlines()

    result = []
    result.append('import tensorflow as tf\n')
    for i in range(len(lines)):
        if function_name == lines[i].strip():
            # if(function_name!=lines[i]):
            #     continue
            print("function_name: ", function_name)
            print("lines[i]: ", lines[i])
            print(lines[i])
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
    print("=======parsed_docstring========")
    parsed_docstring = inspect.getdoc(eval(FUNC_NAME))
    print(parsed_docstring)
    args_section = inspect.signature(eval(FUNC_NAME)).parameters.keys()
    doc_args_section = parsed_docstring.split("Args:\n")[1]
    #returns_section = parsed_docstring.split("Returns:\n")[1]
    print("===============================")
    for pre_re in pre_normalize:
        print("pre_re: ", pre_re)
        #print("ori normalized_text: ", doc_args_section)
        doc_args_section = re.sub(pre_re, pre_normalize[pre_re], doc_args_section, flags=re.IGNORECASE)
        #print("pre normalized_text: ", doc_args_section)

    for arg in args_section:
        arg_description = doc_args_section.split(arg + ":")[1].split("\n")[0].strip()
        arg_description = arg_description.split(".")[0].strip()
        arg_description = arg_description.split(":")[0].strip()
        if(arg != 'name'):
            print("argument: ", arg)
            print("description: ", arg_description)
            if sub_kw(arg_description, 'tensorflow') != None and r'A `Tensor` of' not in arg_description and r'Tensor objects with' not in arg_description and r'tensor' not in arg_description:
                if sub_kw(arg_description, 'tensorflow') in type_map:
                    type_dict[arg] = type_map[sub_kw(arg_description, 'tensorflow')]
            #print("type: ", sub_kw(arg_description, 'tensorflow'))
            print(type_dict)
            print()
    
    if(len(type_dict) == 0):
        print("refind")
        for arg in args_section:
            arg_description = doc_args_section.split(arg + ":")[1].split("\n")[0].strip()
            arg_description = arg_description.split(".")[0].strip()
            arg_description = arg_description.split(":")[0].strip()
            if(arg != 'name'):
                print("argument: ", arg)
                print("description: ", arg_description)
                if sub_kw(arg_description, 'tensorflow') != None:
                    if sub_kw(arg_description, 'tensorflow') in type_map:
                        type_dict[arg] = type_map[sub_kw(arg_description, 'tensorflow')]
                #print("type: ", sub_kw(arg_description, 'tensorflow'))
                print(type_dict)
                print()

    with open('./temp/type_dict.txt', 'w') as file:
        file.write(str(type_dict))

