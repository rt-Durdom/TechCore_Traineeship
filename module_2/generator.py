def read_large_log(file_path):
    with open(file_path, 'r') as file:
        for str_line in file:
            yield str_line
