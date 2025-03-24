# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from evrim import Evrim, AsyncEvrim
from tests.utils import assert_matches_type
from evrim.types.shared import CreatedFieldsToProfile

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCreatedFields:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Evrim) -> None:
        created_field = client.profiles.created_fields.create(
            profile_id="321669910225",
            field_ids=[0],
        )
        assert_matches_type(CreatedFieldsToProfile, created_field, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Evrim) -> None:
        response = client.profiles.created_fields.with_raw_response.create(
            profile_id="321669910225",
            field_ids=[0],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = response.parse()
        assert_matches_type(CreatedFieldsToProfile, created_field, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Evrim) -> None:
        with client.profiles.created_fields.with_streaming_response.create(
            profile_id="321669910225",
            field_ids=[0],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = response.parse()
            assert_matches_type(CreatedFieldsToProfile, created_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Evrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `profile_id` but received ''"):
            client.profiles.created_fields.with_raw_response.create(
                profile_id="",
                field_ids=[0],
            )


class TestAsyncCreatedFields:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncEvrim) -> None:
        created_field = await async_client.profiles.created_fields.create(
            profile_id="321669910225",
            field_ids=[0],
        )
        assert_matches_type(CreatedFieldsToProfile, created_field, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEvrim) -> None:
        response = await async_client.profiles.created_fields.with_raw_response.create(
            profile_id="321669910225",
            field_ids=[0],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        created_field = await response.parse()
        assert_matches_type(CreatedFieldsToProfile, created_field, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEvrim) -> None:
        async with async_client.profiles.created_fields.with_streaming_response.create(
            profile_id="321669910225",
            field_ids=[0],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            created_field = await response.parse()
            assert_matches_type(CreatedFieldsToProfile, created_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncEvrim) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `profile_id` but received ''"):
            await async_client.profiles.created_fields.with_raw_response.create(
                profile_id="",
                field_ids=[0],
            )
