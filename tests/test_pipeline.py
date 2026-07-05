from unittest.mock import MagicMock, patch
import pytest
from app.pipeline.runner import execute_pipeline

TEST_ASSETS = (
    {
        "symbol": "BTC-USDT",
        "name": "Bitcoin",
    },
)


@patch("app.pipeline.runner.BingXProvider")
@patch("app.pipeline.runner.SessionLocal")
@patch("app.pipeline.runner.ETLService")
def test_execute_pipeline_success(
    mock_etl_service_class,
    mock_session_local,
    mock_provider_class,
):
    db = MagicMock()
    mock_session_local.return_value.__enter__.return_value = db

    service = MagicMock()
    run = MagicMock()

    service.etl_runs.start.return_value = run
    service.load_market_data.return_value = 10
    service.calculate_and_save_metrics.return_value = 10
    mock_etl_service_class.return_value = service

    execute_pipeline(TEST_ASSETS)

    mock_provider_class.assert_called_once()
    service.etl_runs.start.assert_called_once()
    service.load_market_data.assert_called_once_with(
        symbol="BTC-USDT",
        name="Bitcoin",
        interval="1d",
        limit=365,
    )
    service.calculate_and_save_metrics.assert_called_once_with("BTC-USDT")
    service.etl_runs.finish.assert_called_once_with(run, 20)
    db.commit.assert_called_once()


@patch("app.pipeline.runner.BingXProvider")
@patch("app.pipeline.runner.SessionLocal")
@patch("app.pipeline.runner.ETLService")
def test_execute_pipeline_failure(
    mock_etl_service_class,
    mock_session_local,
    mock_provider_class,
):
    db = MagicMock()
    mock_session_local.return_value.__enter__.return_value = db

    service = MagicMock()
    run = MagicMock()
    error = RuntimeError("BingX failed")

    service.etl_runs.start.return_value = run
    service.load_market_data.side_effect = error
    mock_etl_service_class.return_value = service

    with pytest.raises(RuntimeError, match="BingX failed"):
        execute_pipeline(TEST_ASSETS)

    mock_provider_class.assert_called_once()
    service.etl_runs.start.assert_called_once()
    service.etl_runs.fail.assert_called_once_with(run, error)
    db.commit.assert_called_once()
