import logging
from opentelemetry import trace
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

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
        zipkin_exporter = ZipkinExporter(
            endpoint=zipkin_endpoint,
        )
        span_processor = BatchSpanProcessor(zipkin_exporter)
        tracer_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(tracer_provider)
        logger.info(f'OpenTelemetry настроен для {service_name},'
                    f' экспорт в Zipkin: {zipkin_endpoint}')

    except Exception as e:
        logger.error(f'Ошибка настройки OpenTelemetry: {e}', exc_info=True)
