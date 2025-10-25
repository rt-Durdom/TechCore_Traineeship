from multiprocessing import Process


def sum_millions():
    print( sum(range(100_000_000)))


if __name__ == '__main__':
    multi_process = Process(target=sum_millions)
    multi_process.start()
    print(multi_process.is_alive())
    multi_process.join()
    if multi_process.is_alive():
        print('Точно завершили расчеты')
