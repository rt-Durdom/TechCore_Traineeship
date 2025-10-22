import json


student = [
    { 'name': 'Иванов', 'avg_grade':  3.4, 'year': 2021 },
    { 'name': 'Петров', 'avg_grade': 4.5, 'year': 2021 },
    { 'name': 'Сидоров', 'avg_grade':  3.9, 'year': 2021 },
    { 'name': 'Васильев', 'avg_grade': 4.9, 'year': 2021 }
]

def serialize_json(student):
    with open('module_1/data_json/config.json ', 'w', encoding='utf-8') as file_json:
        json.dump(student, file_json, indent=4, ensure_ascii=False)

def deserialize_json():
    
    with open('module_1/data_json/config.json ', 'r', encoding='utf-8') as file_json:
        return json.load(file_json)


if __name__ == '__main__':
    serialize_json(student)
    print(deserialize_json())
