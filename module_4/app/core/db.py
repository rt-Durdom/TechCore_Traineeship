import redis

redis_util = redis.asyncio.Redis(host='localhost', port=6379, db=0)


# class Session:
#     def __init__(self):
#         self.conntect = "connection"

#     def responce(self):
#         return "Результат запроса"

#     def close(self):
#         print("Закрываем соединение...")


# def get_db_session():
#     db = Session()
#     try:
#         yield db
#     finally:
#         db.close()
