class DatabaseConnection:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.connect = None

    def __enter__(self):
        try:
            self.connect = self.db_url
            return self.connect
        except Exception as e:
            raise (f'Не подлюключилось, смотри ошибку {e}')

    def __exit__(self, *args, **kwargs):
        try:
            if self.conn:
                self.connect.close()
                self.connect = None
        except Exception as e:
            raise (f'Штатного закрытия не получилось, смотри ошибку {e}')
        finally:
            self.connect.close()
            self.connect = None
            print('Закрыли принудительно')
        

url = "sqlite:///test.db"
with DatabaseConnection(url) as conn:
    pass
