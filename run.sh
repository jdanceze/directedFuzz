#!/bin/bash
for i in {1..20}
do
    find -type f -name '*run_0_1_*' -delete
    #python clear_out_dir_py.py
    python clear_read_dir.py
    echo Running $i >> timeexec.txt
    start=$(date +%s)
    echo "Start: $start" >> timeexec.txt
    timeout 8h python 5_test_case_build_eval_lp_score_exit.py run_0_1 0 1 $i
    end=$(date +%s)
    echo "Stop $end" >> timeexec.txt
    echo "Total: $((end-start))" >> timeexec.txt
    echo "==================">> timeexec.txt
    sleep 15
done