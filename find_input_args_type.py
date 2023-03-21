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
    r'A list of `Tensor`': 'Tensor',
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
    'dictionary' : ('dict')


}

def sub_kw(src_text, framework):
    anno_map = {dtype_anno: [], ds_anno:[]}

    normalized_text = src_text
    dtype_ls = read_yaml('./dtype_ls_tf.yaml')[framework]
    # for pre_re in pre_normalize:
    #     print("pre_re: ", pre_re)
    #     #print("ori normalized_text: ", normalized_text)
    #     normalized_text = re.sub(pre_re, pre_normalize[pre_re], normalized_text, flags=re.IGNORECASE)
    #     #print("pre normalized_text: ", normalized_text)

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
    doc_args_section = parsed_docstring.split("Args:\n")[1]
    #returns_section = parsed_docstring.split("Returns:\n")[1]
    print("===============================")
    dtype_ls = read_yaml('./dtype_ls_tf.yaml')[ 'tensorflow']
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
            if sub_kw(arg_description, 'tensorflow') != None and r'A `Tensor` of' not in arg_description and r'Tensor objects with' not in arg_description:
                if sub_kw(arg_description, 'tensorflow') in type_map:
                    type_dict[arg] = type_map[sub_kw(arg_description, 'tensorflow')]
            #print("type: ", sub_kw(arg_description, 'tensorflow'))
            print(type_dict)

    with open('./temp/type_dict.txt', 'w') as file:
        file.write(str(type_dict))

# tf.raw_ops.MapStage
# tf.compat.v1.extract_volume_patches
#tf.raw_ops.SparseCross
# tf.raw_ops.PyFunc
#tf.raw_ops.UnbatchGrad