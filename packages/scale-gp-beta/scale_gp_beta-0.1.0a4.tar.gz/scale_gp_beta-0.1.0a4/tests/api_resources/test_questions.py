# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import Question
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestQuestions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        question = client.questions.create(
            prompt="prompt",
            title="title",
            type="categorical",
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        question = client.questions.create(
            prompt="prompt",
            title="title",
            type="categorical",
            choices=[
                {
                    "label": "label",
                    "value": "string",
                    "audit_required": True,
                }
            ],
            conditions=[{"foo": "bar"}],
            dropdown=True,
            multi=True,
            number_options={
                "max": 0,
                "min": 0,
            },
            rating_options={
                "max_label": "maxLabel",
                "min_label": "minLabel",
                "scale_steps": 0,
            },
            required=True,
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.questions.with_raw_response.create(
            prompt="prompt",
            title="title",
            type="categorical",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.questions.with_streaming_response.create(
            prompt="prompt",
            title="title",
            type="categorical",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        question = client.questions.retrieve(
            "question_id",
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.questions.with_raw_response.retrieve(
            "question_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.questions.with_streaming_response.retrieve(
            "question_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_id` but received ''"):
            client.questions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        question = client.questions.list()
        assert_matches_type(SyncCursorPage[Question], question, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        question = client.questions.list(
            ending_before="ending_before",
            limit=1,
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorPage[Question], question, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.questions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = response.parse()
        assert_matches_type(SyncCursorPage[Question], question, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.questions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = response.parse()
            assert_matches_type(SyncCursorPage[Question], question, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncQuestions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        question = await async_client.questions.create(
            prompt="prompt",
            title="title",
            type="categorical",
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        question = await async_client.questions.create(
            prompt="prompt",
            title="title",
            type="categorical",
            choices=[
                {
                    "label": "label",
                    "value": "string",
                    "audit_required": True,
                }
            ],
            conditions=[{"foo": "bar"}],
            dropdown=True,
            multi=True,
            number_options={
                "max": 0,
                "min": 0,
            },
            rating_options={
                "max_label": "maxLabel",
                "min_label": "minLabel",
                "scale_steps": 0,
            },
            required=True,
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.questions.with_raw_response.create(
            prompt="prompt",
            title="title",
            type="categorical",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = await response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.questions.with_streaming_response.create(
            prompt="prompt",
            title="title",
            type="categorical",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = await response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        question = await async_client.questions.retrieve(
            "question_id",
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.questions.with_raw_response.retrieve(
            "question_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = await response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.questions.with_streaming_response.retrieve(
            "question_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = await response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_id` but received ''"):
            await async_client.questions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        question = await async_client.questions.list()
        assert_matches_type(AsyncCursorPage[Question], question, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        question = await async_client.questions.list(
            ending_before="ending_before",
            limit=1,
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorPage[Question], question, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.questions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = await response.parse()
        assert_matches_type(AsyncCursorPage[Question], question, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.questions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = await response.parse()
            assert_matches_type(AsyncCursorPage[Question], question, path=["response"])

        assert cast(Any, response.is_closed) is True
