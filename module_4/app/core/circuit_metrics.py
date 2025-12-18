from prometheus_client import Gauge
import pybreaker

# --- Метрика состояния предохранителя ---

_circuit_state_gauge = Gauge(
    name="circuit_breaker_state",
    documentation="Current state of circuit breakers (0=closed, 1=open, 2=half-open)",
    labelnames=["breaker_name"],
)

# Коды состояний
STATE_CLOSED = 0
STATE_OPEN = 1
STATE_HALF_OPEN = 2


def set_circuit_state(breaker_name: str, state: int) -> None:
    """Обновить состояние конкретного Circuit Breaker-а."""
    _circuit_state_gauge.labels(breaker_name=breaker_name).set(state)


# --- Listener для pybreaker, который гонит состояние в Prometheus ---

class BreakerMetricsListener(pybreaker.CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        breaker_name = "book_service"  # имя «предохранителя» на дашборде

        # new_state.name у pybreaker: 'closed', 'open', 'half-open'
        if new_state.name == "closed":
            set_circuit_state(breaker_name, STATE_CLOSED)
        elif new_state.name == "open":
            set_circuit_state(breaker_name, STATE_OPEN)
        elif new_state.name == "half-open":
            set_circuit_state(breaker_name, STATE_HALF_OPEN)
            