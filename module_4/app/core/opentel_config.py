import logging
from opentelemetry import trace, metrics
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider

logger = logging.getLogger(__name__)


def zipkin_sevice(
        service_name: str = 'book-service',
        zipkin_endpoint: str = 'http://zipkin:9411/api/v2/spans'):
    

    try:
        resource = Resource.create({
            'service.name': service_name,
            'service.version': '1.0.0'
        })
        tracer_provider = TracerProvider(resource=resource)
        
        # Настройка метрик для Prometheus
        try:
            metric_reader = PrometheusMetricReader()
            metric_provider = MeterProvider(
                metric_readers=[metric_reader],
                resource=resource
            )
            metrics.set_meter_provider(metric_provider)
            logger.info(f'Prometheus метрики настроены для {service_name}')
        except (ValueError, Exception) as e:
            if "Overriding" in str(e) or "not allowed" in str(e):
                logger.info(f'MeterProvider уже установлен, используем существующий для {service_name}')
            else:
                logger.warning(f'Не удалось установить MeterProvider для {service_name}: {e}')
        zipkin_exporter = ZipkinExporter(
            endpoint=zipkin_endpoint,
        )
        span_processor = BatchSpanProcessor(zipkin_exporter)
        tracer_provider.add_span_processor(span_processor)

        try:
            trace.set_tracer_provider(tracer_provider)
            logger.info(f'OpenTelemetry настроен для {service_name},'
                        f' экспорт в Zipkin: {zipkin_endpoint}')
        except (ValueError, Exception) as e:
            if "Overriding" in str(e) or "not allowed" in str(e):
                logger.info(f'TracerProvider уже установлен, используем существующий для {service_name}')
            else:
                logger.warning(f'Не удалось установить TracerProvider для {service_name}: {e}')

    except Exception as e:
        logger.error(f'Ошибка настройки OpenTelemetry: {e}', exc_info=True)


def get_book_counter():
    try:
        metric = metrics.get_meter_provider().get_meter(
            name='book-service',
            version='1.0.0'
        )

        book_counter = metric.create_counter(
            name='books_created_total',
            description='Счетчик создания книг',
            unit='1'
        )

        logger.info('Счетчик книг создан: books_created')
        return book_counter

    except Exception as e:
        logger.error(f'Ошибка создания счетчика метрик: {e}', exc_info=True)
        return None


_book_counter = None


def get_or_create_book_counter():
    global _book_counter
    if _book_counter is None:
        _book_counter = get_book_counter()
    return _book_counter
