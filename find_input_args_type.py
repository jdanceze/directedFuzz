import sys
import tensorflow as tf
import inspect
import json

from util import * 
import argparse

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
    # r'data\s+type': 'dtype',

}

type_map = {
    'list' : ('list', 'tuple', 'ndarray'),
    'int' : ('int', 'int8', 'int16', 'int32', 'int64'),
    'string' : ('str', 'bytes'),
    'bool' : ('bool', 'bool_')

}

def sub_kw(src_text, framework):
    anno_map = {dtype_anno: [], ds_anno:[]}

    normalized_text = src_text
    dtype_ls = read_yaml('/Users/jdanceze/Desktop/hub/DocTer/constraint_extraction/dtype_ls_tf.yaml')[framework]
    for pre_re in pre_normalize:
        #print("ori normalized_text: ", normalized_text)
        normalized_text = re.sub(pre_re, pre_normalize[pre_re], normalized_text, flags=re.IGNORECASE)
        #print("pre normalized_text: ", normalized_text)

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
    

if __name__ == '__main__':
    type_dict = {}
    #FUNC_NAME = "tf.raw_ops.MapStage"
    FUNC_NAME = sys.argv[1]
    print(FUNC_NAME)
    print("=======parsed_docstring========")
    parsed_docstring = inspect.getdoc(eval(FUNC_NAME))
    print(parsed_docstring)
    args_section = inspect.signature(eval(FUNC_NAME)).parameters.keys()
    returns_section = parsed_docstring.split("Returns:\n")[1]
    print("===============================")
    for arg in args_section:
        arg_description = parsed_docstring.split(arg + ":")[1].split("\n")[0].strip()
        print("argument: ", arg)
        print("description: ", arg_description)
        if sub_kw(arg_description, 'tensorflow') != None:
            type_dict[arg] = type_map[sub_kw(arg_description, 'tensorflow')]
        #print("type: ", sub_kw(arg_description, 'tensorflow'))
        print(type_dict)

    with open('./temp/type_dict.txt', 'w') as file:
        file.write(str(type_dict))

    # with open('./temp/type_dict.txt', 'r') as f:
    #     dict_str = f.read()


    # my_dict = eval(dict_str)

    # print(my_dict['values'])