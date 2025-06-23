import pytest
import json
from aiohttp import web
from rlapi.client import Client
from rlapi.enums import Platform, PlaylistKey
from rlapi.errors import PlayerNotFound
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_client_initialization():
    """Test that the Client initializes correctly."""
    with patch('rlapi.client.Client._get_access_token', new_callable=AsyncMock) as mock_get_token:
        mock_get_token.return_value = "fake_token"
        client = Client(client_id="test_client_id", client_secret="test_client_secret")
        assert client._client_id == "test_client_id"
        assert client._client_secret == "test_client_secret"
        await client.close()


@pytest.mark.asyncio
async def test_get_player_by_id_success():
    """Test successful player lookup by ID."""
    with patch('rlapi.client.Client._get_access_token', new_callable=AsyncMock) as mock_get_token, \
         patch('rlapi.client.Client._request', new_callable=AsyncMock) as mock_request:
        mock_get_token.return_value = "fake_token"
        mock_request.return_value = [json.load(open("tests/fixtures/player_profile.json"))]
        client = Client(client_id="test_client_id", client_secret="test_client_secret")
        player = await client.get_player_by_id(Platform.steam, "76561198012345678")
        assert player.user_name == "TestPlayer"
        assert player.platform == Platform.steam
        assert player.playlists[PlaylistKey.doubles].tier == 21 # Grand Champion is tier 21
        await client.close()


@pytest.mark.asyncio
async def test_get_player_by_id_not_found():
    """Test player not found by ID."""
    with patch('rlapi.client.Client._get_access_token', new_callable=AsyncMock) as mock_get_token, \
         patch('rlapi.client.Client._request', new_callable=AsyncMock) as mock_request:
        mock_get_token.return_value = "fake_token"
        mock_request.return_value = [] # Empty list for not found
        client = Client(client_id="test_client_id", client_secret="test_client_secret")
        with pytest.raises(PlayerNotFound):
            await client.get_player_by_id(Platform.steam, "non_existent_id")
        await client.close()
