from prometheus_fastapi_instrumentator import Instrumentator


def init_metrics(app):
    """Expose /metrics and instrument every route."""
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")
