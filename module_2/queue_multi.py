from multiprocessing import Process, Queue

def func_put(val):
    val.put([42, None, 'Hello world'])

if __name__ == '__main__':
    val = Queue()
    proc_put = Process(target=func_put, args=(val,))

    proc_put.start()
    print(val.get())
    # [42, None, 'Hello world']
    proc_put.join()
