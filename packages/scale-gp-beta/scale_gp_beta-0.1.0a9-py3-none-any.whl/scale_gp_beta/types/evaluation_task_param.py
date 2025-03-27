# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "EvaluationTaskParam",
    "ChatCompletionEvaluationTask",
    "ChatCompletionEvaluationTaskConfiguration",
    "GenericInferenceEvaluationTask",
    "GenericInferenceEvaluationTaskConfiguration",
    "GenericInferenceEvaluationTaskConfigurationInferenceConfiguration",
    "GenericInferenceEvaluationTaskConfigurationInferenceConfigurationLaunchInferenceConfiguration",
    "ApplicationVariantV1EvaluationTask",
    "ApplicationVariantV1EvaluationTaskConfiguration",
    "ApplicationVariantV1EvaluationTaskConfigurationHistoryUnionMember0",
    "ApplicationVariantV1EvaluationTaskConfigurationOverrides",
    "ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides",
    "ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState",
    "ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace",
]


class ChatCompletionEvaluationTaskConfigurationTyped(TypedDict, total=False):
    messages: Required[Union[Iterable[Dict[str, object]], str]]

    model: Required[str]

    audio: Union[Dict[str, object], str]

    frequency_penalty: Union[float, str]

    function_call: Union[Dict[str, object], str]

    functions: Union[Iterable[Dict[str, object]], str]

    logit_bias: Union[Dict[str, int], str]

    logprobs: Union[bool, str]

    max_completion_tokens: Union[int, str]

    max_tokens: Union[int, str]

    metadata: Union[Dict[str, str], str]

    modalities: Union[List[str], str]

    n: Union[int, str]

    parallel_tool_calls: Union[bool, str]

    prediction: Union[Dict[str, object], str]

    presence_penalty: Union[float, str]

    reasoning_effort: str

    response_format: Union[Dict[str, object], str]

    seed: Union[int, str]

    stop: str

    store: Union[bool, str]

    temperature: Union[float, str]

    tool_choice: str

    tools: Union[Iterable[Dict[str, object]], str]

    top_k: Union[int, str]

    top_logprobs: Union[int, str]

    top_p: Union[float, str]


ChatCompletionEvaluationTaskConfiguration: TypeAlias = Union[
    ChatCompletionEvaluationTaskConfigurationTyped, Dict[str, object]
]


class ChatCompletionEvaluationTask(TypedDict, total=False):
    configuration: Required[ChatCompletionEvaluationTaskConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["chat_completion"]


class GenericInferenceEvaluationTaskConfigurationInferenceConfigurationLaunchInferenceConfiguration(
    TypedDict, total=False
):
    num_retries: int

    timeout_seconds: int


GenericInferenceEvaluationTaskConfigurationInferenceConfiguration: TypeAlias = Union[
    GenericInferenceEvaluationTaskConfigurationInferenceConfigurationLaunchInferenceConfiguration, str
]


class GenericInferenceEvaluationTaskConfiguration(TypedDict, total=False):
    model: Required[str]

    args: Union[Dict[str, object], str]

    inference_configuration: GenericInferenceEvaluationTaskConfigurationInferenceConfiguration


class GenericInferenceEvaluationTask(TypedDict, total=False):
    configuration: Required[GenericInferenceEvaluationTaskConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["inference"]


class ApplicationVariantV1EvaluationTaskConfigurationHistoryUnionMember0(TypedDict, total=False):
    request: Required[str]
    """Request inputs"""

    response: Required[str]
    """Response outputs"""

    session_data: Dict[str, object]
    """Session data corresponding to the request response pair"""


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState(
    TypedDict, total=False
):
    current_node: Required[str]

    state: Required[Dict[str, object]]


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace(
    TypedDict, total=False
):
    duration_ms: Required[int]

    node_id: Required[str]

    operation_input: Required[str]

    operation_output: Required[str]

    operation_type: Required[str]

    start_timestamp: Required[str]

    workflow_id: Required[str]

    operation_metadata: Dict[str, object]


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides(TypedDict, total=False):
    concurrent: bool

    initial_state: ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState

    partial_trace: Iterable[
        ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace
    ]

    use_channels: bool


ApplicationVariantV1EvaluationTaskConfigurationOverrides: TypeAlias = Union[
    ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides, str
]


class ApplicationVariantV1EvaluationTaskConfiguration(TypedDict, total=False):
    application_variant_id: Required[str]

    inputs: Required[Union[Dict[str, object], str]]

    history: Union[Iterable[ApplicationVariantV1EvaluationTaskConfigurationHistoryUnionMember0], str]

    operation_metadata: Union[Dict[str, object], str]

    overrides: ApplicationVariantV1EvaluationTaskConfigurationOverrides
    """Execution override options for agentic applications"""


class ApplicationVariantV1EvaluationTask(TypedDict, total=False):
    configuration: Required[ApplicationVariantV1EvaluationTaskConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["application_variant"]


EvaluationTaskParam: TypeAlias = Union[
    ChatCompletionEvaluationTask, GenericInferenceEvaluationTask, ApplicationVariantV1EvaluationTask
]
