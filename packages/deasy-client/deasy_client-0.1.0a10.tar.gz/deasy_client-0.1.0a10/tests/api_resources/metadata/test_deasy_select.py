# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from deasy_client import Deasy, AsyncDeasy
from deasy_client._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeasySelect:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_query(self, client: Deasy) -> None:
        deasy_select = client.metadata.deasy_select.query(
            query="query",
            vdb_profile_name="vdb_profile_name",
        )
        assert_matches_type(object, deasy_select, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_query_with_all_params(self, client: Deasy) -> None:
        deasy_select = client.metadata.deasy_select.query(
            query="query",
            vdb_profile_name="vdb_profile_name",
            columns=["id"],
            data_description="data_description",
            tag_names=["string"],
            tag_schemas=[
                {
                    "description": "description",
                    "name": "name",
                    "output_type": "output_type",
                    "available_values": ["string"],
                    "created_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "date_format": "date_format",
                    "examples": ["string"],
                    "max_values": 0,
                    "neg_examples": ["string"],
                    "retry_feedback": {},
                    "tag_id": "tag_id",
                    "tuned": 0,
                    "updated_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "username": "username",
                }
            ],
            top_k=0,
        )
        assert_matches_type(object, deasy_select, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_query(self, client: Deasy) -> None:
        response = client.metadata.deasy_select.with_raw_response.query(
            query="query",
            vdb_profile_name="vdb_profile_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deasy_select = response.parse()
        assert_matches_type(object, deasy_select, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_query(self, client: Deasy) -> None:
        with client.metadata.deasy_select.with_streaming_response.query(
            query="query",
            vdb_profile_name="vdb_profile_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deasy_select = response.parse()
            assert_matches_type(object, deasy_select, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDeasySelect:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_query(self, async_client: AsyncDeasy) -> None:
        deasy_select = await async_client.metadata.deasy_select.query(
            query="query",
            vdb_profile_name="vdb_profile_name",
        )
        assert_matches_type(object, deasy_select, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncDeasy) -> None:
        deasy_select = await async_client.metadata.deasy_select.query(
            query="query",
            vdb_profile_name="vdb_profile_name",
            columns=["id"],
            data_description="data_description",
            tag_names=["string"],
            tag_schemas=[
                {
                    "description": "description",
                    "name": "name",
                    "output_type": "output_type",
                    "available_values": ["string"],
                    "created_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "date_format": "date_format",
                    "examples": ["string"],
                    "max_values": 0,
                    "neg_examples": ["string"],
                    "retry_feedback": {},
                    "tag_id": "tag_id",
                    "tuned": 0,
                    "updated_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "username": "username",
                }
            ],
            top_k=0,
        )
        assert_matches_type(object, deasy_select, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_query(self, async_client: AsyncDeasy) -> None:
        response = await async_client.metadata.deasy_select.with_raw_response.query(
            query="query",
            vdb_profile_name="vdb_profile_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deasy_select = await response.parse()
        assert_matches_type(object, deasy_select, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncDeasy) -> None:
        async with async_client.metadata.deasy_select.with_streaming_response.query(
            query="query",
            vdb_profile_name="vdb_profile_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deasy_select = await response.parse()
            assert_matches_type(object, deasy_select, path=["response"])

        assert cast(Any, response.is_closed) is True
