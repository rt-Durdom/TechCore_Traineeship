import time


def timer(func):
    def wrapper():
        start_time = time.time()
        func()
        end_time = time.time()
        print(f"Execution time: {(end_time - start_time):.1f}s")
    return wrapper

@timer
def sleep():
    time.sleep(1)
    print('Завершили работу')


sleep()
