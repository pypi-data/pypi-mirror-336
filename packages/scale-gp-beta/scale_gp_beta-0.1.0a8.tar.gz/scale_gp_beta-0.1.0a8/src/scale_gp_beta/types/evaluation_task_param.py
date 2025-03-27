# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "EvaluationTaskParam",
    "ChatCompletionEvaluationTaskRequest",
    "ChatCompletionEvaluationTaskRequestConfiguration",
    "GenericInferenceEvaluationTaskRequest",
    "GenericInferenceEvaluationTaskRequestConfiguration",
    "GenericInferenceEvaluationTaskRequestConfigurationInferenceConfiguration",
    "GenericInferenceEvaluationTaskRequestConfigurationInferenceConfigurationLaunchInferenceConfiguration",
    "ApplicationVariantV1EvaluationTaskRequest",
    "ApplicationVariantV1EvaluationTaskRequestConfiguration",
    "ApplicationVariantV1EvaluationTaskRequestConfigurationHistoryUnionMember0",
    "ApplicationVariantV1EvaluationTaskRequestConfigurationOverrides",
    "ApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverrides",
    "ApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesInitialState",
    "ApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesPartialTrace",
]


class ChatCompletionEvaluationTaskRequestConfigurationTyped(TypedDict, total=False):
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


ChatCompletionEvaluationTaskRequestConfiguration: TypeAlias = Union[
    ChatCompletionEvaluationTaskRequestConfigurationTyped, Dict[str, object]
]


class ChatCompletionEvaluationTaskRequest(TypedDict, total=False):
    configuration: Required[ChatCompletionEvaluationTaskRequestConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["chat_completion"]


class GenericInferenceEvaluationTaskRequestConfigurationInferenceConfigurationLaunchInferenceConfiguration(
    TypedDict, total=False
):
    num_retries: int

    timeout_seconds: int


GenericInferenceEvaluationTaskRequestConfigurationInferenceConfiguration: TypeAlias = Union[
    GenericInferenceEvaluationTaskRequestConfigurationInferenceConfigurationLaunchInferenceConfiguration, str
]


class GenericInferenceEvaluationTaskRequestConfiguration(TypedDict, total=False):
    model: Required[str]

    args: Union[Dict[str, object], str]

    inference_configuration: GenericInferenceEvaluationTaskRequestConfigurationInferenceConfiguration


class GenericInferenceEvaluationTaskRequest(TypedDict, total=False):
    configuration: Required[GenericInferenceEvaluationTaskRequestConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["inference"]


class ApplicationVariantV1EvaluationTaskRequestConfigurationHistoryUnionMember0(TypedDict, total=False):
    request: Required[str]
    """Request inputs"""

    response: Required[str]
    """Response outputs"""

    session_data: Dict[str, object]
    """Session data corresponding to the request response pair"""


class ApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesInitialState(
    TypedDict, total=False
):
    current_node: Required[str]

    state: Required[Dict[str, object]]


class ApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesPartialTrace(
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


class ApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverrides(
    TypedDict, total=False
):
    concurrent: bool

    initial_state: (
        ApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesInitialState
    )

    partial_trace: Iterable[
        ApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesPartialTrace
    ]

    use_channels: bool


ApplicationVariantV1EvaluationTaskRequestConfigurationOverrides: TypeAlias = Union[
    ApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverrides, str
]


class ApplicationVariantV1EvaluationTaskRequestConfiguration(TypedDict, total=False):
    application_variant_id: Required[str]

    inputs: Required[Union[Dict[str, object], str]]

    history: Union[Iterable[ApplicationVariantV1EvaluationTaskRequestConfigurationHistoryUnionMember0], str]

    operation_metadata: Union[Dict[str, object], str]

    overrides: ApplicationVariantV1EvaluationTaskRequestConfigurationOverrides
    """Execution override options for agentic applications"""


class ApplicationVariantV1EvaluationTaskRequest(TypedDict, total=False):
    configuration: Required[ApplicationVariantV1EvaluationTaskRequestConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["application_variant"]


EvaluationTaskParam: TypeAlias = Union[
    ChatCompletionEvaluationTaskRequest,
    GenericInferenceEvaluationTaskRequest,
    ApplicationVariantV1EvaluationTaskRequest,
]
