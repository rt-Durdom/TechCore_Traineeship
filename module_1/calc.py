def verify(x):
    
    if x.isalpha():
        return x
    if x.find('.') != -1:
        return float(x)
    else:
        return int(x)

def calc(a, b, operator: str):
    a = verify(a)
    b = verify(b)

    if operator == '+':
        return a + b
    if (isinstance(a, (int)) or isinstance(b, (int))) and operator == '*':
        return a * b
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if operator == '-':
            return a - b

        # Выполнено задание поиск с помощьью отладчика, выявлен недостаток - деление на 0
        # Исправляется с помощью try/except
        if operator == '/':
            try:
                return a / b
            except ZeroDivisionError:
                raise ZeroDivisionError('Деление на ноль невозможно!')
        if operator == '*':
            return a * b

    else:
        return 'Что-то пошло не так!'

if __name__ == "__main__":
    a = input('Введите 1-ое значение: ')
    b = input('Введите 2-ое значение:')
    operator = input('Введите оператор *, +, - или /: ')

    print(calc(a, b, operator))
