import os
import concurrent.futures

# list of strings to search in the GitHub Advisory database
strings_to_search = ['tf.raw_ops.DecodeJpeg', 'tf.raw_ops.LookupTableExportV2', 'tf.raw_ops.SobolSample', 'tf.raw_ops.TensorSummaryV2']
path_to_database_directory = '/Users/jdanceze/Downloads/advisory-database-main/advisories'
found_count = 0
print("Total: ", len(strings_to_search))
def get_advisory_files():
    advisory_files = []
    for root, dirs, files in os.walk(path_to_database_directory):
        for file in files:
            if file.endswith('.json'):
                advisory_files.append(os.path.join(root, file))
    return advisory_files
    
def search_advisory_file(advisory_file):
    global found_count
    
    for string in strings_to_search:
        #strings_to_search.remove(string)
        found = False
        with open(advisory_file, 'r') as f:
            if string in f.read():
                found = True
                print("Found: ", string)
                # print("File: ", advisory_file)
                # print(" ")
        if found:
            found_count += 1
            strings_to_search.remove(string)


def search_advisory_files(advisory_files):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(search_advisory_file, advisory_files)


advisory_files = get_advisory_files()
print("finished get_advisory_files")
search_advisory_files(advisory_files)

print("Found count: ", found_count)
