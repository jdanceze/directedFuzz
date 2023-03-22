import json
import time
import re
import os

gen_path = "/opt/homebrew/Caskroom/miniforge/base/lib/python3.10/site-packages/tensorflow/python/"
target_function_namespace = "tensorflow::Tensor::scalar"

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
    class_list = []
    interface_list = set()
    function_interface_list = []
    with open('./temp/depth_1_dict.json') as json_file:
        dictionary = json.load(json_file)

    result = find_keys_with_value(dictionary, target_function_namespace)
    # with open('./temp/top_function.txt', 'w') as f:
    #   #f.write(str(keep_namespace))
    #   f.write(str(result))

    end_time = time.time()
    print("time: ", end_time - start_time)

    #result = ['tensorflow::anonymous_namespace{example_proto_helper_test::cc}::SingleExampleProtoToTensorsTest::SetUp', 'tensorflow::BroadcastToOp::Compute', 'tensorflow::functor::BincountFunctor&lt; CPUDevice, Tidx, T, false &gt;::Compute', 'tensorflow::QuantizedRelu6Op::Compute', 'tensorflow::PriorityQueue::TryEnqueueMany', 'tensorflow::barrier::Barrier::TryInsertMany', 'tensorflow::InTopK', 'tensorflow::anonymous_namespace{resource_ops_test::cc}::MockHandleCreationOpKernel::Compute', 'tensorflow::XRTCompileOp::Compute', 'tensorflow::SwitchOp::Compute', 'tensorflow::data::IteratorFromStringHandleOp::Compute', 'tensorflow::CSRZerosOp::Compute', 'tensorflow::graph_transforms::QuantizeWeights', 'tensorflow::graph_transforms::QuantizeWeightsTest::TestQuantizeWeights', 'tensorflow::anonymous_namespace{restore_v2_op_test::cc}::RestoreV2OpTest::RunTest', 'tensorflow::WriteHistogramSummaryOp::Compute', 'tensorflow::SaveV2::Compute', 'tensorflow::OneHot', 'tensorflow::fuzzing::FuzzOneHot::BuildGraph', 'tensorflow::AdjustContrastOp::Compute', 'tensorflow::InitializeTableFromTextFileOp::Compute', 'tensorflow::grappler::ConstantFolding::SimplifyCase', 'tensorflow::grappler::ConstantFolding::SimplifyNode', 'tensorflow::grappler::ConstantFolding::SimplifyGraph', 'tensorflow::grappler::ConstantFolding::RunOptimizationPass', 'tensorflow::grappler::ConstantFolding::Optimize', 'tensorflow::grappler::anonymous_namespace{constant_folding_test::cc}::ConstantFoldingTest::SimpleNeutralElementTest', 'tensorflow::grappler::anonymous_namespace{constant_folding_test::cc}::ConstantFoldingCastConstTest::ConstantFoldingOptimize', 'tensorflow::grappler::anonymous_namespace{constant_folding_test::cc}::ConstantFoldingTest::PaddingWithZeroSize', 'tensorflow::grappler::anonymous_namespace{constant_folding_test::cc}::ConstantFoldingTest::MulConvPushDownTest', 'tensorflow::anonymous_namespace{functional_ops::cc}::ForOp::State::State']
    result = [x for x in result if "Compute" in x]
    
    print(result)
    for element in result:
        print("bef: ", element)
        element = re.sub(r'\{.*?\}', '', element)
        print("After: ", element)
        parts = element.split('::')
        class_name = parts[len(parts)-2]
        func_name = parts[len(parts)-1]
        print(f"class element: {class_name}, function element: {func_name}")
        class_list.append(class_name)
        print()

    print(class_list)

    with open('found_class.txt', 'r') as f:
        lines = f.readlines()
    for class_name_each in class_list:
        for line in lines:
            parts = line.strip().split(',')
            filename = parts[0]
            function_name = parts[1]
            class_name = parts[2]
            if class_name_each == class_name:
                print(f"Found class: {class_name}")
                interface_list.add(function_name)
                
    print(interface_list)

    for function_interface in interface_list:
        function_interface = function_interface + ' ='
        print("Finding: ", function_interface)

        for root, dirs, files in os.walk(gen_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            for line_number, line in enumerate(f):
                                if function_interface in line:

                                    if "gen_" not in file:
                                        print("This is not gen file")
                                        print("Skipping: ", file)
                                    else:
                                        print("================Regis=====================")
                                        print("Found: ", function_interface)
                                        print("File Path: ", file_path)
                                        print("File: ", file)
                                        print("Line number: ", line_number + 1)
                                        print("Line: ", line)
                                        #target_register_op = line.split('=')[0].strip()
                                        target_register_op = "tf." + line[line.find('"')+1:line.rfind('"')]
                                        print("Target: ", target_register_op)
                                        function_interface_list.append(target_register_op)
                                        break
                                    #print(f"File: {file_path}, Line {line_number + 1}: {line}")
    with open('./temp/function_for_test.txt', 'w') as f:
      #f.write(str(keep_namespace))
      f.write(str(function_interface_list))
    print(len(function_interface_list))
    end_time = time.time()
    print("time: ", end_time - start_time)



    