import os
import natsort

final_time = []
result_dir = '/result_s_TensorListScatter/'
time_file_name = 'timeexec_s_TensorListScatter.txt'

with open(time_file_name) as f:

    start = [line[7:-1] for line in f if line.startswith("Start:")]
    print("Number of start: ", len(start))
    print(", ".join(start))


list_of_files = os.listdir(result_dir)
sorted_list_of_files = natsort.natsorted(list_of_files)

for file in sorted_list_of_files:
    #print(file)
    with open(result_dir + file) as f:

        final = [line[12:-1].split(".")[0] for line in f if line.startswith("Final time:")]
        final_time.append(final[len(final) - 1])
        #print(final[len(final) - 1])

print("Number of final: ", len(final_time))
#print(start)
print(final_time)

minus = [int(final_time[i]) - int(start[i]) for i in range(len(start))]
print("Number of minus: ", len(minus))
print(minus)