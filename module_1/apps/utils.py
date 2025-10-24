def logger(message, *args, **kwargs):
    x = args
    y = {k:v for k, v in kwargs.items()}
    print(f'{message}\n'
          f'{x}\n'
          f'{y}')