import logging


def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_logging_configuration():
    logger = logging.getLogger("uvicorn")
    assert logger is not None
    assert logger.level == logging.INFO
