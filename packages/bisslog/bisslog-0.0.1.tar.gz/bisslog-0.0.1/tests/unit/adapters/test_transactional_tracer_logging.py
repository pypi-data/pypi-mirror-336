import logging
from unittest.mock import MagicMock, patch
import pytest
from bisslog.adapters.tracing.transactional_tracer_logging import TransactionalTracerLogging

@pytest.fixture
def tracer():
    return TransactionalTracerLogging()

@pytest.fixture
def mock_logger(tracer):
    tracer._logger = MagicMock()
    return tracer._logger

@pytest.mark.parametrize("method, log_level", [
    ("info", "info"),
    ("debug", "debug"),
    ("warning", "warning"),
    ("error", "error"),
    ("critical", "critical"),
    ("func_error", "error"),
    ("tech_error", "critical"),
    ("report_start_external", "info"),
    ("report_end_external", "info"),
])
def test_logging_methods(tracer, mock_logger, method, log_level):
    payload = "Test log message"
    transaction_id = "tx-123"
    checkpoint_id = "chk-456"
    extra = {"key": "value"}

    with patch.object(tracer, "_re_args_with_main", return_value={"transaction_id": transaction_id, "checkpoint_id": checkpoint_id}):
        getattr(tracer, method)(payload, transaction_id=transaction_id, checkpoint_id=checkpoint_id, extra=extra)

    expected_extra = {"transaction_id": transaction_id, "checkpoint_id": checkpoint_id, **extra}
    log_method = getattr(mock_logger, log_level)
    log_method.assert_called_once_with(payload, extra=expected_extra)
