"""
This script is a proof of concept for fetching images from DeviantArt.
It demonstrates how to use the DeviantArt API to retrieve a list of images based on a search query.
The script is intended for testing and demonstration purposes only, and should not be used in
production without proper error handling and API rate limiting.
"""

import json
import os
from typing import List

import dotenv
import httpx
import pytest

dotenv.load_dotenv()


class DeviantArtClient:
    BASE_URL = "https://www.deviantart.com/api/v1/oauth2"

    def __init__(self, token_url: str, client_id: str, client_secret: str):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None

    async def authenticate(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            response.raise_for_status()
            data = response.json()
            self.access_token = data["access_token"]

    async def call_placebo(self):
        url = f"{self.BASE_URL}/placebo"
        params = {"access_token": self.access_token}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def search_images(self, offset: int = 0, query: str = "", limit: int = 10):
        url = f"{self.BASE_URL}/browse/home"
        params = {
            "offset": offset,
            "limit": limit,
            "q": query,
            "access_token": self.access_token,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def get_deviations_metadata(self, deviationids: List[str]):
        url = f"{self.BASE_URL}/deviation/metadata"
        params = {
            "deviationids": deviationids,
            "access_token": self.access_token,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def get_additional_deviation_metadata(self, deviationid: str):
        url = f"{self.BASE_URL}/deviation/{deviationid}"
        params = {
            "access_token": self.access_token,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def get_user_collections(self, username: str, offset: int = 0, limit: int = 10):
        url = f"{self.BASE_URL}/collections/all"
        params = {
            "username": username,
            "offset": offset,
            "limit": limit,
            "access_token": self.access_token,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def get_user_galleries(self, username: str, offset: int = 0, limit: int = 10):
        url = f"{self.BASE_URL}/gallery/all"
        params = {
            "username": username,
            "offset": offset,
            "limit": limit,
            "access_token": self.access_token,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()


async def test_authentication():
    client_id = os.getenv("DEVIANTART_CLIENT_ID")
    client_secret = os.getenv("DEVIANTART_CLIENT_SECRET")
    token_url = "https://www.deviantart.com/oauth2/token"

    client = DeviantArtClient(token_url, client_id, client_secret)
    await client.authenticate()

    assert client.access_token is not None
    await client.call_placebo()  # This will raise an exception if the token is invalid


@pytest.mark.asyncio
async def test_deviantart_fetch():
    client_id = os.getenv("DEVIANTART_CLIENT_ID")
    client_secret = os.getenv("DEVIANTART_CLIENT_SECRET")
    token_url = "https://www.deviantart.com/oauth2/token"

    client = DeviantArtClient(token_url, client_id, client_secret)
    await client.authenticate()
    results = await client.search_images(query="landscape", limit=5)

    assert "results" in results
    assert len(results["results"]) > 0


@pytest.mark.asyncio
async def test_can_generate_example_result_file():
    client_id = os.getenv("DEVIANTART_CLIENT_ID")
    client_secret = os.getenv("DEVIANTART_CLIENT_SECRET")
    token_url = "https://www.deviantart.com/oauth2/token"

    client = DeviantArtClient(token_url, client_id, client_secret)
    await client.authenticate()
    results = await client.search_images(limit=5)

    with open("tmp/example_deviantart_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)


@pytest.mark.asyncio
async def test_can_generate_example_result_metadata_file():
    client_id = os.getenv("DEVIANTART_CLIENT_ID")
    client_secret = os.getenv("DEVIANTART_CLIENT_SECRET")
    token_url = "https://www.deviantart.com/oauth2/token"

    client = DeviantArtClient(token_url, client_id, client_secret)
    await client.authenticate()
    search_results = await client.search_images(limit=5)
    deviation_ids = [result["deviationid"] for result in search_results["results"]]
    metadata_results = await client.get_deviations_metadata(deviation_ids)

    with open("tmp/example_deviantart_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata_results, f, indent=4)


@pytest.mark.asyncio
async def test_can_fetch_user_galleries():
    client_id = os.getenv("DEVIANTART_CLIENT_ID")
    client_secret = os.getenv("DEVIANTART_CLIENT_SECRET")
    token_url = "https://www.deviantart.com/oauth2/token"

    client = DeviantArtClient(token_url, client_id, client_secret)
    await client.authenticate()
    username = "tuckspickets"
    galleries_result = await client.get_user_galleries(username)

    assert "results" in galleries_result
    assert isinstance(galleries_result["results"], list)


@pytest.mark.asyncio
async def test_can_fetch_user_galleries_and_generate_example_file():
    client_id = os.getenv("DEVIANTART_CLIENT_ID")
    client_secret = os.getenv("DEVIANTART_CLIENT_SECRET")
    token_url = "https://www.deviantart.com/oauth2/token"

    client = DeviantArtClient(token_url, client_id, client_secret)
    await client.authenticate()
    username = "tuckspickets"
    galleries_result = await client.get_user_galleries(username)

    with open("tmp/example_deviantart_galleries.json", "w", encoding="utf-8") as f:
        json.dump(galleries_result, f, indent=4)


@pytest.mark.asyncio
async def test_can_fetch_user_collections():
    client_id = os.getenv("DEVIANTART_CLIENT_ID")
    client_secret = os.getenv("DEVIANTART_CLIENT_SECRET")
    token_url = "https://www.deviantart.com/oauth2/token"

    client = DeviantArtClient(token_url, client_id, client_secret)
    await client.authenticate()
    username = "tuckspickets"
    collections_result = await client.get_user_collections(username)

    assert "results" in collections_result
    assert isinstance(collections_result["results"], list)


@pytest.mark.asyncio
async def test_can_generate_example_user_collections_file():
    client_id = os.getenv("DEVIANTART_CLIENT_ID")
    client_secret = os.getenv("DEVIANTART_CLIENT_SECRET")
    token_url = "https://www.deviantart.com/oauth2/token"

    client = DeviantArtClient(token_url, client_id, client_secret)
    await client.authenticate()
    username = "tuckspickets"
    collections_result = await client.get_user_collections(username)

    with open("tmp/example_deviantart_collections.json", "w", encoding="utf-8") as f:
        json.dump(collections_result, f, indent=4)


@pytest.mark.asyncio
async def test_can_fetch_specific_deviation_metadata():
    client_id = os.getenv("DEVIANTART_CLIENT_ID")
    client_secret = os.getenv("DEVIANTART_CLIENT_SECRET")
    token_url = "https://www.deviantart.com/oauth2/token"

    client = DeviantArtClient(token_url, client_id, client_secret)
    await client.authenticate()
    deviation_id = "BD6437E7-B81A-D9D8-A2C3-FE1A6B138DE8"
    metadata_result = await client.get_deviations_metadata([deviation_id])

    assert "metadata" in metadata_result
    assert metadata_result["metadata"][0]["deviationid"] == deviation_id


@pytest.mark.asyncio
async def test_can_generate_example_specific_deviation_metadata_file():
    client_id = os.getenv("DEVIANTART_CLIENT_ID")
    client_secret = os.getenv("DEVIANTART_CLIENT_SECRET")
    token_url = "https://www.deviantart.com/oauth2/token"

    client = DeviantArtClient(token_url, client_id, client_secret)
    await client.authenticate()
    deviation_id = "FFF2B9F2-E89A-2189-5296-7072414A89E2"
    metadata_result = await client.get_deviations_metadata([deviation_id])

    with open("tmp/example_specific_deviation_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata_result, f, indent=4)


@pytest.mark.asyncio
async def test_deviantart_media_has_all_mandatory_fields():
    galeriafora_external_media_map = {
        "url": "content.src",
        "title": "title",
        "description": "description",
        "tags": "tags.tag_name",
        "rating": "is_mature",
        "ai_metadata.is_ai_generated": None,  # DeviantArt doesn't provide this information, so we will set it to None
        "content_metadata.content_type": "content.src",  # Need to determine the content type based on the file extension
        "content_metadata.dimensions.width": "content.width",
        "content_metadata.dimensions.height": "content.height",
        "content_metadata.file_size": "content.filesize",
    }

    def path_exists(data, path):
        keys = path.split(".")
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            elif isinstance(data, list):
                # If it's a list, we need to check if all items have the key (for tags)
                if all(isinstance(item, dict) and key in item for item in data):
                    data = [item[key] for item in data]
                else:
                    return False
            else:
                return False
        return True

    client_id = os.getenv("DEVIANTART_CLIENT_ID")
    client_secret = os.getenv("DEVIANTART_CLIENT_SECRET")

    token_url = "https://www.deviantart.com/oauth2/token"
    client = DeviantArtClient(token_url, client_id, client_secret)
    await client.authenticate()
    deviation_id = "FFF2B9F2-E89A-2189-5296-7072414A89E2"
    metadata_result = await client.get_deviations_metadata([deviation_id])

    deviation_additional_metadata = await client.get_additional_deviation_metadata(deviation_id)
    deviation_metadata = metadata_result["metadata"][0]

    # Check if deviantart fields defined above are present at least in one of the two metadata responses
    for galeria_field, deviant_field in galeriafora_external_media_map.items():
        if deviant_field is None:
            continue  # Skip fields that are not provided by DeviantArt
        assert path_exists(deviation_metadata, deviant_field) or path_exists(
            deviation_additional_metadata, deviant_field
        ), f"Field {deviant_field} for {galeria_field} not found in metadata"

    # Additional check for content_type: ensure content.src exists and can derive type from extension
    assert path_exists(deviation_metadata, "content.src") or path_exists(
        deviation_additional_metadata, "content.src"
    ), "content.src not found for content_type derivation"
