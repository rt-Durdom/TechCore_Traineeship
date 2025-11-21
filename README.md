#Работа по тестированию навыков.

Будут публиковаться отдельные пааки (модули), в которых будут выполняться различные тестовые задания от простых к сложным.

- в задании модуля 5 Асинхронные Транзакции и FastAPI Depends (DI для сессии) - уже на этапе подготовки CRUD и engine был примененн механизм атомарности за счет менеждера и внедрения зависимостей. НУ так получилось, Рука набита сразу это делать.))))

- запуск selery с логированием:
    celery -A new_app_celery worker --loglevel=info #терминал 1
    python cel_main.py #терминал 2 - вызов задачи
- для запуска веб сервера:
    uvicorn main:app --reload
- для запуска flower:
    celery -A new_app_celery flower

- находясь в папке app (сруктура app/grpc/...) выполняется команда на компиляцию grpc файлов.
python -m grpc_tools.protoc \
    -I grpc \
    --python_out=grpc \
    --grpc_python_out=grpc \
    grpc/book.proto

