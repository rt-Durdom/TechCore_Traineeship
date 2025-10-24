from apps.utils import logger


if __name__ == "__main__":
    mes = 'Hello world'
    a = 2
    b = 3
    c = 4

    logger(mes, a, b, c, {'1': 'a', '2': 'b', '3': 'c'}, v=6)
    logger('Test', 1, 2, user='admin')
