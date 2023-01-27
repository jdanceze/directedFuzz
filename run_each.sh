#!/bin/bash
python clear_out_dir.py
python clear_read_dir.py
python 5_test_case_build_eval_lp_score_exit.py run_0_1 0 1 | tee "01TensorListConcat_score_exit_1.txt"