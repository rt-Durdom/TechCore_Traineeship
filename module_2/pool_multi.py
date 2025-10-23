import multiprocessing


def heavy_task(_):
    return sum(range(100_000_000))


if __name__ == "__main__":
    tasks_list = list(range(1, 11))

    count_core = multiprocessing.cpu_count()

    pool = multiprocessing.Pool(processes=count_core)
    res = list(pool.map(heavy_task, tasks_list))

    print(f'Ядер процессора задействовано: {count_core}')
    print(*res)
