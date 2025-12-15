import logging
import sys

import structlog


def setup_logging(service_name: str) -> None:
    """
    Глобальная настройка логирования:
    - stdlib logging -> через structlog -> JSON в stdout
    - все существующие logging.getLogger(...) продолжают работать
    """

    timestamper = structlog.processors.TimeStamper(fmt="iso")

    # Настраиваем structlog (уровень "логическая" обработка)
    structlog.configure(
        processors=[
            # Добавляем имя логгера и уровень
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            # Обёртка, чтобы ProcessorFormatter мог дальше отрендерить
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Formatter, который уже делает финальный JSON
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(),  # финальный вид лога
        foreign_pre_chain=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            timestamper,
        ],
    )

    # Хэндлер на stdout (для Docker/prome/promtail)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Подменяем root-логгер (и, по сути, всё stdlib-logging)
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    # Добавим контекст сервиса (будет видно в JSON как "service": "book-service")
    structlog.get_logger().bind(service=service_name)