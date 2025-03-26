"""Unit tests for the generations module."""

from uuid import uuid4
from typing import Any, cast
from functools import cached_property
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import computed_field
from mirascope import llm
from mirascope.core import BaseTool, BaseMessageParam, BaseDynamicConfig
from mirascope.core.base import (
    Metadata,
    BaseCallParams,
    BaseCallResponse,
)
from mirascope.core.base.types import CostMetadata, FinishReason
from mirascope.core.base._utils import BaseMessageParamConverter
from mirascope.llm.call_response import CallResponse

from lilypad import Message
from lilypad.lib.generations import (
    generation,
    _build_mirascope_call,
)
from lilypad.types.ee.projects import CommonCallParams, GenerationPublic

dummy_spans = []


@pytest.fixture
def dummy_generation_instance() -> GenerationPublic:
    """Return a dummy GenerationPublic instance."""
    return GenerationPublic(
        uuid=str(uuid4()),
        name="dummy_generation",
        signature="dummy_signature",
        code="def dummy(): pass",
        hash="dummy_hash",
        dependencies={},
        arg_types={},
        version_num=1,
        call_params=CommonCallParams(),
        provider="openai",
        model="gpt-4o-mini",
    )


class DummySpanContext:
    """A dummy span context."""

    @property
    def trace_id(self) -> int:
        """Return a dummy trace ID."""
        return 1234567890

    @property
    def span_id(self) -> int:
        """Return a dummy span ID."""
        return 9876543210


class DummySpan:
    """A dummy span that records its name and attributes."""

    def __init__(self, name: str):
        self.name = name
        self.attributes = {}
        dummy_spans.append(self)

    def set_attribute(self, key: str, value: any) -> None:  # pyright: ignore [reportGeneralTypeIssues]
        """Set a single attribute."""
        self.attributes[key] = value

    def set_attributes(self, attrs: dict) -> None:
        """Set multiple attributes at once."""
        self.attributes.update(attrs)

    def get_span_context(self) -> DummySpanContext:
        """Return a dummy span context."""
        return DummySpanContext()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        pass


class DummyTracer:
    """A dummy tracer that returns DummySpan instances."""

    def start_as_current_span(self, name: str):
        """Start a new span and return it."""
        return DummySpan(name)


@pytest.fixture(autouse=True)
def reset_dummies(monkeypatch):
    """Reset the dummy spans and the global counter before each test."""
    dummy_spans.clear()
    # Reset the global counter in the traces module.
    monkeypatch.setattr("lilypad.lib.traces._span_counter", 0)


@pytest.fixture(autouse=True)
def patch_get_tracer(monkeypatch):
    """Patch the get_tracer method to return a DummyTracer instance."""
    monkeypatch.setattr("lilypad.lib.traces.get_tracer", lambda _: DummyTracer())


@generation()
def sync_outer(param: str) -> str:
    """A synchronous function that calls two other synchronous functions."""
    return "sync outer"


@pytest.fixture
def fake_closure_fixture():
    """Fixture that returns a fake Closure.from_code function."""

    def fake_closure_from_code(code: str, name: str, dependencies=None):
        class DummyClosure:
            def build_object(self):
                return f"dummy_object_for_{name}"

        return DummyClosure()

    return fake_closure_from_code


@pytest.fixture
def fake_llm_call_fixture(dummy_call_response_instance):
    """Fixture that returns a fake llm.call function for sync branch."""

    def fake_llm_call(**kwargs):
        def inner(mirascope_prompt):
            return lambda *args, **kwargs: dummy_call_response_instance

        return inner

    return fake_llm_call


@pytest.fixture
def patched_llm_call(fake_llm_call_fixture, monkeypatch):
    """Fixture that patches llm.call with fake_llm_call_fixture for sync branch."""
    monkeypatch.setattr(llm, "call", fake_llm_call_fixture)


class DummyCallParams(BaseCallParams):
    """A dummy call params class."""

    pass


class DummyMessageParam(BaseMessageParam):
    """A dummy message param class."""

    role: str
    content: Any


class DummyMessageParamConverter(BaseMessageParamConverter):
    """Base class for converting message params to/from provider formats."""

    @staticmethod
    def to_provider(message_params: list[BaseMessageParam]) -> list[Any]:
        """Converts base message params -> provider-specific messages."""
        return []

    @staticmethod
    def from_provider(message_params: list[Any]) -> list[BaseMessageParam]:
        """Converts provider-specific messages -> Base message params."""
        return []


class DummyTool(BaseTool):
    """A dummy tool class."""

    def call(self):
        """Call the tool."""
        ...

    @property
    def model_fields(self):  # pyright: ignore [reportIncompatibleVariableOverride]
        """Return a list of model fields."""
        return ["field1"]

    field1: str = "tool_field"


class DummyProviderCallResponse(
    BaseCallResponse[
        Any,
        DummyTool,
        Any,
        BaseDynamicConfig,
        DummyMessageParam,
        DummyCallParams,
        DummyMessageParam,
        DummyMessageParamConverter,
    ]
):
    """A dummy provider call response class."""

    _message_converter: type[DummyMessageParamConverter] = DummyMessageParamConverter

    @property
    def content(self) -> str:
        """Return the content of the response."""
        return "dummy_content"

    @property
    def finish_reasons(self) -> list[str] | None:
        """Return a list of finish reasons."""
        return ["finish"]

    @property
    def model(self) -> str | None:
        """Return the model of the response."""
        ...

    @property
    def id(self) -> str | None:
        """Return the ID of the response."""
        ...

    @property
    def usage(self) -> Any:
        """Return a dummy usage instance."""
        ...

    @property
    def input_tokens(self) -> int | float | None:
        """Should return the number of input tokens."""
        ...

    @property
    def output_tokens(self) -> int | float | None:
        """Should return the number of output tokens."""
        ...

    @property
    def cost(self) -> float | None:
        """Should return the cost of the response in dollars."""
        ...

    @property
    def cached_tokens(self) -> int | None:
        """Returns the number of cached tokens."""
        pass

    @property
    def cost_metadata(self) -> CostMetadata:
        """Returns the cost of the response in dollars."""
        return CostMetadata(
            input_tokens=self.input_tokens,
            output_tokens=self.output_tokens,
            cached_tokens=self.cached_tokens,
        )

    @computed_field
    @cached_property
    def message_param(self) -> Any:
        """Return a dummy message param."""
        return BaseMessageParam(role="assistant", content="dummy_content")

    @computed_field
    @cached_property
    def tools(self) -> list[DummyTool] | None:
        """Return a list of dummy tools."""
        return [DummyTool()]

    @computed_field
    @cached_property
    def tool(self) -> DummyTool | None:
        """Return a dummy tool."""
        return DummyTool()

    @classmethod
    def tool_message_params(cls, tools_and_outputs: list[tuple[DummyTool, str]]) -> list[Any]:
        """Return a list of tool message params."""
        ...

    @property
    def common_finish_reasons(self) -> list[FinishReason] | None:
        """Return a list of finish reasons."""
        return cast(list[FinishReason], self.finish_reasons)

    @property
    def common_message_param(self):
        """Return a dummy message param."""
        return BaseMessageParam(role="assistant", content="common_message")

    @property
    def common_user_message_param(self):
        """Return a dummy user message param."""
        return BaseMessageParam(role="user", content="common_user_message")

    @property
    def common_usage(self):
        """Return a dummy usage instance."""
        ...

    def common_construct_message_param(self, tool_calls: list[Any] | None, content: str | None):
        """Return a dummy CallResponse instance."""
        ...


@pytest.fixture
def dummy_call_response_instance():
    """Return a dummy CallResponse instance."""
    dummy_response = DummyProviderCallResponse(
        metadata=Metadata(),
        response={},
        tool_types=None,
        prompt_template=None,
        fn_args={},
        dynamic_config={},
        messages=[],
        call_params=DummyCallParams(),
        call_kwargs={},
        user_message_param=None,
        start_time=0,
        end_time=0,
    )
    return CallResponse(response=dummy_response)  # pyright: ignore [reportAbstractUsage,reportArgumentType]


@pytest.fixture
def fake_llm_call_async_fixture(dummy_call_response_instance: CallResponse):
    """Fixture that returns a fake llm.call function for async branch."""

    def fake_llm_call_async(**kwargs):
        def inner(mirascope_prompt):
            return lambda *args, **kwargs: dummy_call_response_instance

        return inner

    return fake_llm_call_async


@pytest.fixture
def patched_llm_call_async(fake_llm_call_async_fixture, monkeypatch):
    """Fixture that patches llm.call with fake_llm_call_async_fixture for async branch."""
    monkeypatch.setattr(llm, "call", fake_llm_call_async_fixture)


@generation()
async def async_outer(param: str) -> str:
    """An asynchronous function that calls two other asynchronous functions."""
    return "async outer"


def fake_mirascope_middleware_sync(generation, arg_values, is_async, prompt_template, span_context_holder):
    """Simulate a synchronous mirascope middleware returning a dummy result."""

    def middleware(fn):
        def wrapped(*args, **kwargs):
            return "managed sync result"

        return wrapped

    return middleware


def fake_mirascope_middleware_async(generation, arg_values, is_async, prompt_template, span_context_holder):
    """Simulate an asynchronous mirascope middleware returning a dummy result."""

    def middleware(fn):
        async def wrapped(*args, **kwargs):
            return "managed async result"

        return wrapped

    return middleware


def fake_llm_call(**kwargs):
    """Fake llm.call which ignores its arguments and returns a dummy callable."""

    def inner(mirascope_prompt):
        return lambda *args, **kwargs: dummy_call_response_instance

    return inner


def fake_llm_call_async(**kwargs):
    """Fake llm.call which ignores its arguments and returns a dummy callable."""

    def inner(mirascope_prompt):
        return lambda *args, **kwargs: "managed async result"

    return inner


@pytest.fixture
def mock_lilypad_client(dummy_generation_instance: GenerationPublic) -> MagicMock:
    mock_client = MagicMock()

    mock_name = MagicMock()
    mock_name.retrieve_by_version.return_value = dummy_generation_instance
    mock_name.retrieve_deployed.return_value = dummy_generation_instance

    mock_generations = MagicMock()
    mock_generations.name = mock_name
    mock_generations.retrieve_by_hash.return_value = dummy_generation_instance

    mock_projects = MagicMock()
    mock_projects.generations = mock_generations

    mock_client.projects = mock_projects
    return mock_client


@pytest.fixture
def mock_async_lilypad_client(dummy_generation_instance: GenerationPublic) -> AsyncMock:
    mock_client = AsyncMock()

    mock_name = MagicMock()
    mock_name.retrieve_by_version = AsyncMock(return_value=dummy_generation_instance)
    mock_name.retrieve_deployed = AsyncMock(return_value=dummy_generation_instance)

    mock_generations = MagicMock()
    mock_generations.name = mock_name
    mock_generations.retrieve_by_hash = AsyncMock(return_value=dummy_generation_instance)

    mock_projects = MagicMock()
    mock_projects.generations = mock_generations

    mock_client.projects = mock_projects
    return mock_client


def test_sync_managed_generation(
    dummy_generation_instance: GenerationPublic, dummy_call_response_instance, mock_lilypad_client
):
    mock_client = mock_lilypad_client
    with (
        patch("lilypad.lib.generations.Lilypad", return_value=mock_client),
        patch("lilypad.lib.generations.llm.call") as mock_llm_call,
    ):
        mock_mirascope_call = MagicMock()
        mock_inner = MagicMock()
        mock_llm_call.return_value = mock_mirascope_call
        mock_mirascope_call.return_value = mock_inner
        mock_inner.return_value = dummy_call_response_instance

        @generation(managed=True)
        def managed_sync(param: str) -> str:
            return "should not be used"

        result = managed_sync("dummy")
        assert isinstance(result, Message)
        assert result.content == "dummy_content"
        mock_client.projects.generations.name.retrieve_deployed.assert_called_once()


def test_sync_mirascope_attr(dummy_generation_instance: GenerationPublic):
    """Test that a synchronous function with __mirascope_call__ set follows the mirascope branch."""

    def base_sync(param: str) -> str:
        return "should not be used"

    base_sync.__mirascope_call__ = True  # pyright: ignore [reportFunctionMemberAccess]

    mock_lilypad = MagicMock()
    mock_lilypad.projects.generations.name.retrieve_by_version.return_value = dummy_generation_instance

    with (
        patch("lilypad.lib.generations.create_mirascope_middleware", side_effect=fake_mirascope_middleware_sync),
        patch("lilypad.lib.generations.Lilypad", return_value=mock_lilypad),
        patch("lilypad.lib.generations.llm.call", side_effect=fake_llm_call),
    ):
        decorated = generation()(base_sync)
        result = decorated("dummy")
        assert result == "managed sync result"


@pytest.mark.asyncio
async def test_async_mirascope_attr(dummy_generation_instance: GenerationPublic):
    """Test that an asynchronous function with __mirascope_call__ set follows the mirascope branch."""

    async def base_async(param: str) -> str:
        return "should not be used"

    base_async.__mirascope_call__ = True  # pyright: ignore [reportFunctionMemberAccess]

    mock_async_lilypad = AsyncMock()
    mock_async_lilypad.projects.generations.name.retrieve_by_version.return_value = dummy_generation_instance

    with (
        patch("lilypad.lib.generations.create_mirascope_middleware", side_effect=fake_mirascope_middleware_async),
        patch("lilypad.lib.generations.AsyncLilypad", return_value=mock_async_lilypad),
        patch("lilypad.lib.generations.llm.call", side_effect=fake_llm_call),
    ):
        decorated = generation()(base_async)
        result = await decorated("dummy")
        assert result == "managed async result"


def test_build_mirascope_call_async(dummy_generation_instance: GenerationPublic, patched_llm_call_async):
    """Test _build_mirascope_call branch async call."""
    dummy_generation_instance.prompt_template = "dummy_template"

    async def dummy_fn():
        return None

    result = _build_mirascope_call(dummy_generation_instance, dummy_fn)
    assert result().content == "dummy_content"  # pyright: ignore [reportAttributeAccessIssue]


def test_build_mirascope_call_sync(dummy_generation_instance: GenerationPublic, patched_llm_call):
    """Test _build_mirascope_call branch sync call."""
    dummy_generation_instance.prompt_template = "dummy_template"

    def dummy_fn():
        return None

    result = _build_mirascope_call(dummy_generation_instance, dummy_fn)
    assert result().content == "dummy_content"


def test_build_mirascope_call_invalid_model(dummy_generation_instance: GenerationPublic):
    """Test that _build_mirascope_call raises ValueError when the GenerationPublic instance is missing model or provider."""
    invalid_gen = dummy_generation_instance.model_copy()
    invalid_gen.model = None
    with pytest.raises(ValueError, match="Managed generation requires `model`"):
        _build_mirascope_call(invalid_gen, lambda: None)
    # Now test with a missing provider.
    invalid_gen = dummy_generation_instance.model_copy()
    invalid_gen.provider = None
    with pytest.raises(ValueError, match="Managed generation requires `provider`"):
        _build_mirascope_call(invalid_gen, lambda: None)
