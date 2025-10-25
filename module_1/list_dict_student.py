student = [
    {'name': 'Иванов', 'avg_grade':  3.4},
    {'name': 'Петров', 'avg_grade': 4.5},
    {'name': 'Сидоров', 'avg_grade':  3.9},
    {'name': 'Васильев', 'avg_grade': 4.9}]


def student_filter(student):
    """Функция фильтрации студентов."""
    print(list(filter(lambda x: x['avg_grade'] > 4.0, student)))


if __name__ == '__main__':
    student_filter(student)
