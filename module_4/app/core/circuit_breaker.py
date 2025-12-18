import pybreaker
from module_4.app.core.circuit_metrics import (
    BreakerMetricsListener, STATE_CLOSED, set_circuit_state
)

book_service_breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=30,
    listeners=[BreakerMetricsListener()],
)


set_circuit_state("book_service", STATE_CLOSED)
