from tasks import process_order

if __name__ == '__main__':
    res = process_order.delay(1)

    print(res)
