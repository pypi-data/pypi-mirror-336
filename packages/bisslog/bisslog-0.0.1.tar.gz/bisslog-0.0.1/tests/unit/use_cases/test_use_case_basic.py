import pytest
from unittest.mock import MagicMock, patch

from bisslog.use_cases.use_case_basic import BasicUseCase
from ..utils.fake_tracer import FakeTracer


class SampleUseCase(BasicUseCase):
    """Sample subclass for testing BasicUseCase."""

    @BasicUseCase._transaction_manager.getter
    def transaction_manager(self):
        return MagicMock()

    @BasicUseCase._tracing_opener.getter
    def transaction_manager(self):
        return MagicMock()

    @BasicUseCase.log.getter
    def transaction_manager(self):
        return FakeTracer()

    def use(self, *args, **kwargs):
        """Mock implementation of the 'use' method."""
        return "use_case_result"


@pytest.fixture
def use_case():
    """Fixture to provide a BasicUseCase instance with mocked dependencies."""
    return SampleUseCase("test_use_case")


def test_use_case_call(use_case):
    """Ensures calling the use case triggers the 'use' method."""
    result = use_case()
    assert result == "use_case_result"


def test_start_transaction(use_case):
    """Tests if a transaction is correctly started."""
    use_case._transaction_manager.create_transaction_id = MagicMock()
    use_case._transaction_manager.create_transaction_id.return_value = "tx-123"
    use_case._tracing_opener.start = MagicMock()

    transaction_id = use_case._BasicUseCase__start()

    assert transaction_id == "tx-123"
    use_case._tracing_opener.start.assert_called_once()


def test_end_transaction(use_case):
    """Tests if a transaction ends correctly."""
    use_case._transaction_manager.close_transaction = MagicMock()
    use_case._tracing_opener.end = MagicMock()

    use_case._BasicUseCase__end("tx-123", "super-tx-456", "result")

    use_case._transaction_manager.close_transaction.assert_called_once()
    use_case._tracing_opener.end.assert_called_once_with(
        transaction_id="tx-123", component="test_use_case",
        super_transaction_id="super-tx-456", result="result"
    )


def test_use_case_exception_handling(use_case):
    """Ensures exceptions are logged and re-raised."""
    use_case.use = MagicMock(side_effect=ValueError("test error"))
    use_case.log.tech_error = MagicMock()

    with pytest.raises(ValueError, match="test error"):
        use_case()

    use_case.log.tech_error.assert_called_once()
