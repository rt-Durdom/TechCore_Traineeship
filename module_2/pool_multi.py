import multiprocessing


def heavy_task():
    return sum(range(100_000_000))


if __name__ == "__main__":
    tasks = list(range(1, 11))

    cpu_count = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=cpu_count) as pool:
        results = pool.map(heavy_task, tasks)
    print(f'Ядер процессора задействовано: {cpu_count}')
    for result in results:
        print(result)
