#!/bin/bash
#python cg_find_top_function.py
list=($(sed "s/[][]//g;s/,$//;s/,//g;s/'//g" temp/function_for_test.txt))
if [ ${#list[@]} -eq 0 ]; then
    echo "The list is empty"
else
    count=1
    for item in "${list[@]}"
    do
        echo $item
        python find_input_args_type.py $item
        #timeout 1000 python 5_test_case_build_eval_lp_valid_exit_condi.py run_0_1 0 1 $count
        echo $count
        ((count++))
        #./port.sh
        #sleep 10
    done
fi