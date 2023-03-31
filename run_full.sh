#!/bin/bash
start=$(date +%s)
echo "Start: $start" >> timeexec.txt
for i in {0..1}
do
   find -type f -name 'synthesized_lp_test_run_0_1_*' -delete
   find -type f -name 'lp_run_0_1_*' -delete
   find -type f -name 'debug_run_0_1_*' -delete
   find -type f -name 'outcomes_run_0_1_*' -delete
   find -type f -name 'synthesized_all_lp_test_run_0_1_0_1_*' -delete
   timeout 540 python 5_test_case_build_eval_lp.py run_0_1 0 100 $i
   ./port.sh
   sleep 20
done
end=$(date +%s)
echo "Stop $end" >> timeexec.txt
echo "Total: $((end-start))" >> timeexec.txt
echo "==================">> timeexec.txt
