

def read_large_log(file_path):
    with open(file_path, 'r') as file:
        for str_line in file:
            yield str_line


file_path = 'module_2/data_txt/text.txt'
line_in_file = read_large_log(file_path)

print(next(line_in_file))
# первая строка 
print(next(line_in_file))
# вторая строка и т.д.
