input_file = 'all_functions.txt'
output_base_name = './partition/'
delimiter = "========="
count = 0
output_index = 0

with open(input_file, "r") as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    if "=" in lines[i]:
        count += 1
        if count % 100 == 0:  # reached every 5th delimiter
            output_file = output_base_name + str(output_index) + ".txt"
            with open(output_file, "w") as f:
                f.write("".join(lines[:i+1]))  # write content up to the delimiter
            output_index += 1
            lines = lines[i+1:]
            i = 0  # reset index to start from beginning of new list
            continue  # restart loop
    i += 1
            
if lines:  # write any remaining content to a final file
    output_file = output_base_name + str(output_index) + ".txt"
    with open(output_file, "w") as f:
        f.write("".join(lines))
print("count: ",count)