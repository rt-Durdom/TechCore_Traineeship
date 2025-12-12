from module_4.app.core.opentel_config import zipkin_sevice

# Настраиваем трейсинг для analytics-worker-async
# KafkaInstrumentor не работает с aiokafka/confluent-kafka, поэтому убираем
zipkin_sevice(
    service_name="analytics-worker-async", 
    zipkin_endpoint="http://zipkin:9411/api/v2/spans"
)
