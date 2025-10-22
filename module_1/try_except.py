import logging


def open_file():
    try:
        with open('module_1/data_txt/data.txt', 'r') as file:
            print(file.read())
            logging.info('Файл успешно открыт.')
    except FileNotFoundError as not_f:
        logging.error(not_f)
        raise FileNotFoundError('Файл не найден.')
    except PermissionError as perm:
        logging.error(perm)
        raise PermissionError('Нет прав на чтение.')
    except Exception as ex:
        logging.error(ex)
        raise Exception('Что-то пошло не так.')
    finally:
        print('Done. В любом случае это выполнится')


if __name__ == '__main__':
    open_file()
