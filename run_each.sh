#!/bin/bash
for i in {1..1}
do
    #find -type f -name '*run_0_1_*' -delete
    echo Running $i >> timeexec.txt
    start=$(date +%s)
    echo "Start: $start" >> timeexec.txt
    timeout 1000 python 5_test_case_build_eval_lp_valid_exit_condi.py run_0_1 0 1 $i
    end=$(date +%s)
    echo "Stop $end" >> timeexec.txt
    echo "Total: $((end-start))" >> timeexec.txt
    echo "==================">> timeexec.txt
    ./port.sh
    sleep 10
done