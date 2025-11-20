from module_4.app_celery.new_app_celery import celery_app


@celery_app.task
def nightly_report():
    return 'Отчет за ночь'
