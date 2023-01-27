#!/bin/bash
for i in {1..5}
do
    echo Running $i >> timeexec.txt
    start=$(date +%s)
    echo "Start: $start" >> timeexec.txt
    python 5_test_case_build_eval_lp_score_exit.py run_0_1 0 1 $i
    sleep 2
    end=$(date +%s)
    echo "Stop $end" >> timeexec.txt
    echo "Total: $((end-start))" >> timeexec.txt
    echo "==================">> timeexec.txt
done