import json
import pytest
from aiohttp import ClientSession
from unittest.mock import AsyncMock, patch

from rlapi.config import PsynetConfig
from rlapi.errors import HTTPException


@pytest.fixture
def mock_session():
    return AsyncMock(spec=ClientSession)


@pytest.mark.asyncio
async def test_psynet_config_fetch_success(mock_session):
    mock_response_data = {"PlayerTitles": {"title1": {}, "title2": {}}, "Population": {"pop1": 100}}
    mock_session.get.return_value.__aenter__.return_value.status = 200
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(mock_response_data)
    )
    mock_session.get.return_value.__aenter__.return_value.headers = {
        "Content-Type": "application/json"
    }

    config = PsynetConfig(mock_session)
    data = await config.fetch_config()

    assert data == mock_response_data
    mock_session.get.assert_called_once_with(
        f"{PsynetConfig.BASE_URL}/{PsynetConfig.BUILD_ID}/"
        f"{PsynetConfig.PLATFORM}/{PsynetConfig.REGION}/{PsynetConfig.LANGUAGE}/"
    )


@pytest.mark.asyncio
async def test_psynet_config_fetch_http_error(mock_session):
    mock_session.get.return_value.__aenter__.return_value.status = 404
    mock_session.get.return_value.__aenter__.return_value.text.return_value = (
        "Not Found"
    )

    config = PsynetConfig(mock_session)
    with pytest.raises(HTTPException):
        await config.fetch_config()


@pytest.mark.asyncio
async def test_psynet_config_fetch_retry(mock_session):
    # First two attempts fail with 500, third succeeds
    mock_session.get.return_value.__aenter__.side_effect = [
        AsyncMock(status=500, text=AsyncMock(return_value="Internal Server Error")),
        AsyncMock(status=500, text=AsyncMock(return_value="Internal Server Error")),
        AsyncMock(
            status=200, json=AsyncMock(return_value={"PlayerTitles": {}, "Population": {}})
        ),
    ]

    config = PsynetConfig(mock_session)
    await config.fetch_config()

    assert mock_session.get.call_count == 3


@pytest.mark.asyncio
async def test_psynet_config_get_player_titles_data(mock_session):
    mock_response_data = {"PlayerTitles": {"title1": {}, "title2": {}}, "Population": {"pop1": 100}}
    mock_session.get.return_value.__aenter__.return_value.status = 200
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(mock_response_data)
    )
    mock_session.get.return_value.__aenter__.return_value.headers = {
        "Content-Type": "application/json"
    }

    config = PsynetConfig(mock_session)
    await config.fetch_config()  # Populate cache

    titles_data = config.get_player_titles_data()
    assert titles_data == {"title1": {}, "title2": {}}


@pytest.mark.asyncio
async def test_psynet_config_get_population_data(mock_session):
    mock_response_data = {"PlayerTitles": {"title1": {}, "title2": {}}, "Population": {"pop1": 100}}
    mock_session.get.return_value.__aenter__.return_value.status = 200
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(mock_response_data)
    )
    mock_session.get.return_value.__aenter__.return_value.headers = {
        "Content-Type": "application/json"
    }

    config = PsynetConfig(mock_session)
    await config.fetch_config()  # Populate cache

    population_data = config.get_population_data()
    assert population_data == {"pop1": 100}


@pytest.mark.asyncio
async def test_psynet_config_cache(mock_session):
    mock_response_data_first = {"PlayerTitles": {"title1": {}}, "Population": {"pop1": 100}}
    mock_response_data_second = {"PlayerTitles": {"title3": {}}, "Population": {"pop2": 200}}

    # First call to fetch_config
    mock_session.get.return_value.__aenter__.return_value.status = 200
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(mock_response_data_first)
    )
    mock_session.get.return_value.__aenter__.return_value.headers = {
        "Content-Type": "application/json"
    }
    config = PsynetConfig(mock_session)
    first_data = await config.fetch_config()
    assert first_data == mock_response_data_first
    mock_session.get.call_count = 0  # Reset call count for cache test

    # Second call within cache duration, should use cache
    with patch(
        "time.time",
        return_value=config._last_fetch_time + config._cache_duration - 10,  # type: ignore
    ):
        cached_data = await config.fetch_config()
        assert cached_data == mock_response_data_first
        assert mock_session.get.call_count == 0  # No new HTTP request

    # Third call after cache duration, should fetch again
    with patch(
        "time.time",
        return_value=config._last_fetch_time + config._cache_duration + 10,  # type: ignore
    ):
        mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
            return_value=json.dumps(mock_response_data_second)
        )
        mock_session.get.return_value.__aenter__.return_value.headers = {
            "Content-Type": "application/json"
        }
        new_data = await config.fetch_config()
        assert new_data == mock_response_data_second
        assert mock_session.get.call_count == 1  # New HTTP request
