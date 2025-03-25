# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "EvaluationCreateParams",
    "EvaluationStandaloneCreateRequest",
    "EvaluationStandaloneCreateRequestTask",
    "EvaluationStandaloneCreateRequestTaskChatCompletionEvaluationTaskRequest",
    "EvaluationStandaloneCreateRequestTaskChatCompletionEvaluationTaskRequestConfiguration",
    "EvaluationStandaloneCreateRequestTaskGenericInferenceEvaluationTaskRequest",
    "EvaluationStandaloneCreateRequestTaskGenericInferenceEvaluationTaskRequestConfiguration",
    "EvaluationStandaloneCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfiguration",
    "EvaluationStandaloneCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfigurationLaunchInferenceConfiguration",
    "EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequest",
    "EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfiguration",
    "EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationHistoryUnionMember0",
    "EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverrides",
    "EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverrides",
    "EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesInitialState",
    "EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesPartialTrace",
    "EvaluationFromDatasetCreateRequest",
    "EvaluationFromDatasetCreateRequestData",
    "EvaluationFromDatasetCreateRequestTask",
    "EvaluationFromDatasetCreateRequestTaskChatCompletionEvaluationTaskRequest",
    "EvaluationFromDatasetCreateRequestTaskChatCompletionEvaluationTaskRequestConfiguration",
    "EvaluationFromDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequest",
    "EvaluationFromDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfiguration",
    "EvaluationFromDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfiguration",
    "EvaluationFromDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfigurationLaunchInferenceConfiguration",
    "EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequest",
    "EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfiguration",
    "EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationHistoryUnionMember0",
    "EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverrides",
    "EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverrides",
    "EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesInitialState",
    "EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesPartialTrace",
    "EvaluationWithDatasetCreateRequest",
    "EvaluationWithDatasetCreateRequestDataset",
    "EvaluationWithDatasetCreateRequestTask",
    "EvaluationWithDatasetCreateRequestTaskChatCompletionEvaluationTaskRequest",
    "EvaluationWithDatasetCreateRequestTaskChatCompletionEvaluationTaskRequestConfiguration",
    "EvaluationWithDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequest",
    "EvaluationWithDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfiguration",
    "EvaluationWithDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfiguration",
    "EvaluationWithDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfigurationLaunchInferenceConfiguration",
    "EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequest",
    "EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfiguration",
    "EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationHistoryUnionMember0",
    "EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverrides",
    "EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverrides",
    "EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesInitialState",
    "EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesPartialTrace",
]


class EvaluationStandaloneCreateRequest(TypedDict, total=False):
    data: Required[Iterable[Dict[str, object]]]
    """Items to be evaluated"""

    name: Required[str]

    description: str

    tasks: Iterable[EvaluationStandaloneCreateRequestTask]
    """Tasks allow you to augment and evaluate your data"""


class EvaluationStandaloneCreateRequestTaskChatCompletionEvaluationTaskRequestConfigurationTyped(
    TypedDict, total=False
):
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


EvaluationStandaloneCreateRequestTaskChatCompletionEvaluationTaskRequestConfiguration: TypeAlias = Union[
    EvaluationStandaloneCreateRequestTaskChatCompletionEvaluationTaskRequestConfigurationTyped, Dict[str, object]
]


class EvaluationStandaloneCreateRequestTaskChatCompletionEvaluationTaskRequest(TypedDict, total=False):
    configuration: Required[EvaluationStandaloneCreateRequestTaskChatCompletionEvaluationTaskRequestConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["chat_completion"]


class EvaluationStandaloneCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfigurationLaunchInferenceConfiguration(
    TypedDict, total=False
):
    num_retries: int

    timeout_seconds: int


EvaluationStandaloneCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfiguration: TypeAlias = Union[
    EvaluationStandaloneCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfigurationLaunchInferenceConfiguration,
    str,
]


class EvaluationStandaloneCreateRequestTaskGenericInferenceEvaluationTaskRequestConfiguration(TypedDict, total=False):
    model: Required[str]

    args: Union[Dict[str, object], str]

    inference_configuration: (
        EvaluationStandaloneCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfiguration
    )


class EvaluationStandaloneCreateRequestTaskGenericInferenceEvaluationTaskRequest(TypedDict, total=False):
    configuration: Required[EvaluationStandaloneCreateRequestTaskGenericInferenceEvaluationTaskRequestConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["inference"]


class EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationHistoryUnionMember0(
    TypedDict, total=False
):
    request: Required[str]
    """Request inputs"""

    response: Required[str]
    """Response outputs"""

    session_data: Dict[str, object]
    """Session data corresponding to the request response pair"""


class EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesInitialState(
    TypedDict, total=False
):
    current_node: Required[str]

    state: Required[Dict[str, object]]


class EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesPartialTrace(
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


class EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverrides(
    TypedDict, total=False
):
    concurrent: bool

    initial_state: EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesInitialState

    partial_trace: Iterable[
        EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesPartialTrace
    ]

    use_channels: bool


EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverrides: TypeAlias = Union[
    EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverrides,
    str,
]


class EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfiguration(
    TypedDict, total=False
):
    application_variant_id: Required[str]

    inputs: Required[Union[Dict[str, object], str]]

    history: Union[
        Iterable[
            EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationHistoryUnionMember0
        ],
        str,
    ]

    operation_metadata: Union[Dict[str, object], str]

    overrides: EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverrides
    """Execution override options for agentic applications"""


class EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequest(TypedDict, total=False):
    configuration: Required[EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["application_variant"]


EvaluationStandaloneCreateRequestTask: TypeAlias = Union[
    EvaluationStandaloneCreateRequestTaskChatCompletionEvaluationTaskRequest,
    EvaluationStandaloneCreateRequestTaskGenericInferenceEvaluationTaskRequest,
    EvaluationStandaloneCreateRequestTaskApplicationVariantV1EvaluationTaskRequest,
]


class EvaluationFromDatasetCreateRequest(TypedDict, total=False):
    data: Required[Iterable[EvaluationFromDatasetCreateRequestData]]
    """Items to be evaluated, including references to the input dataset items"""

    dataset_id: Required[str]
    """The ID of the dataset containing the items referenced by the `data` field"""

    name: Required[str]

    description: str

    tasks: Iterable[EvaluationFromDatasetCreateRequestTask]
    """Tasks allow you to augment and evaluate your data"""


class EvaluationFromDatasetCreateRequestDataTyped(TypedDict, total=False):
    dataset_item_id: Required[str]


EvaluationFromDatasetCreateRequestData: TypeAlias = Union[
    EvaluationFromDatasetCreateRequestDataTyped, Dict[str, object]
]


class EvaluationFromDatasetCreateRequestTaskChatCompletionEvaluationTaskRequestConfigurationTyped(
    TypedDict, total=False
):
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


EvaluationFromDatasetCreateRequestTaskChatCompletionEvaluationTaskRequestConfiguration: TypeAlias = Union[
    EvaluationFromDatasetCreateRequestTaskChatCompletionEvaluationTaskRequestConfigurationTyped, Dict[str, object]
]


class EvaluationFromDatasetCreateRequestTaskChatCompletionEvaluationTaskRequest(TypedDict, total=False):
    configuration: Required[EvaluationFromDatasetCreateRequestTaskChatCompletionEvaluationTaskRequestConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["chat_completion"]


class EvaluationFromDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfigurationLaunchInferenceConfiguration(
    TypedDict, total=False
):
    num_retries: int

    timeout_seconds: int


EvaluationFromDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfiguration: TypeAlias = Union[
    EvaluationFromDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfigurationLaunchInferenceConfiguration,
    str,
]


class EvaluationFromDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfiguration(TypedDict, total=False):
    model: Required[str]

    args: Union[Dict[str, object], str]

    inference_configuration: (
        EvaluationFromDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfiguration
    )


class EvaluationFromDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequest(TypedDict, total=False):
    configuration: Required[EvaluationFromDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["inference"]


class EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationHistoryUnionMember0(
    TypedDict, total=False
):
    request: Required[str]
    """Request inputs"""

    response: Required[str]
    """Response outputs"""

    session_data: Dict[str, object]
    """Session data corresponding to the request response pair"""


class EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesInitialState(
    TypedDict, total=False
):
    current_node: Required[str]

    state: Required[Dict[str, object]]


class EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesPartialTrace(
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


class EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverrides(
    TypedDict, total=False
):
    concurrent: bool

    initial_state: EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesInitialState

    partial_trace: Iterable[
        EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesPartialTrace
    ]

    use_channels: bool


EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverrides: TypeAlias = Union[
    EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverrides,
    str,
]


class EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfiguration(
    TypedDict, total=False
):
    application_variant_id: Required[str]

    inputs: Required[Union[Dict[str, object], str]]

    history: Union[
        Iterable[
            EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationHistoryUnionMember0
        ],
        str,
    ]

    operation_metadata: Union[Dict[str, object], str]

    overrides: EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverrides
    """Execution override options for agentic applications"""


class EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequest(TypedDict, total=False):
    configuration: Required[
        EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfiguration
    ]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["application_variant"]


EvaluationFromDatasetCreateRequestTask: TypeAlias = Union[
    EvaluationFromDatasetCreateRequestTaskChatCompletionEvaluationTaskRequest,
    EvaluationFromDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequest,
    EvaluationFromDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequest,
]


class EvaluationWithDatasetCreateRequest(TypedDict, total=False):
    data: Required[Iterable[Dict[str, object]]]
    """Items to be evaluated"""

    dataset: Required[EvaluationWithDatasetCreateRequestDataset]
    """Create a reusable dataset from items in the `data` field"""

    name: Required[str]

    description: str

    tasks: Iterable[EvaluationWithDatasetCreateRequestTask]
    """Tasks allow you to augment and evaluate your data"""


class EvaluationWithDatasetCreateRequestDataset(TypedDict, total=False):
    name: Required[str]

    description: str

    keys: List[str]
    """Keys from items in the `data` field that should be included in the dataset.

    If not provided, all keys will be included.
    """


class EvaluationWithDatasetCreateRequestTaskChatCompletionEvaluationTaskRequestConfigurationTyped(
    TypedDict, total=False
):
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


EvaluationWithDatasetCreateRequestTaskChatCompletionEvaluationTaskRequestConfiguration: TypeAlias = Union[
    EvaluationWithDatasetCreateRequestTaskChatCompletionEvaluationTaskRequestConfigurationTyped, Dict[str, object]
]


class EvaluationWithDatasetCreateRequestTaskChatCompletionEvaluationTaskRequest(TypedDict, total=False):
    configuration: Required[EvaluationWithDatasetCreateRequestTaskChatCompletionEvaluationTaskRequestConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["chat_completion"]


class EvaluationWithDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfigurationLaunchInferenceConfiguration(
    TypedDict, total=False
):
    num_retries: int

    timeout_seconds: int


EvaluationWithDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfiguration: TypeAlias = Union[
    EvaluationWithDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfigurationLaunchInferenceConfiguration,
    str,
]


class EvaluationWithDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfiguration(TypedDict, total=False):
    model: Required[str]

    args: Union[Dict[str, object], str]

    inference_configuration: (
        EvaluationWithDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfigurationInferenceConfiguration
    )


class EvaluationWithDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequest(TypedDict, total=False):
    configuration: Required[EvaluationWithDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequestConfiguration]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["inference"]


class EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationHistoryUnionMember0(
    TypedDict, total=False
):
    request: Required[str]
    """Request inputs"""

    response: Required[str]
    """Response outputs"""

    session_data: Dict[str, object]
    """Session data corresponding to the request response pair"""


class EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesInitialState(
    TypedDict, total=False
):
    current_node: Required[str]

    state: Required[Dict[str, object]]


class EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesPartialTrace(
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


class EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverrides(
    TypedDict, total=False
):
    concurrent: bool

    initial_state: EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesInitialState

    partial_trace: Iterable[
        EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverridesPartialTrace
    ]

    use_channels: bool


EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverrides: TypeAlias = Union[
    EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverridesAgenticApplicationOverrides,
    str,
]


class EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfiguration(
    TypedDict, total=False
):
    application_variant_id: Required[str]

    inputs: Required[Union[Dict[str, object], str]]

    history: Union[
        Iterable[
            EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationHistoryUnionMember0
        ],
        str,
    ]

    operation_metadata: Union[Dict[str, object], str]

    overrides: EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfigurationOverrides
    """Execution override options for agentic applications"""


class EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequest(TypedDict, total=False):
    configuration: Required[
        EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequestConfiguration
    ]

    alias: str
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Literal["application_variant"]


EvaluationWithDatasetCreateRequestTask: TypeAlias = Union[
    EvaluationWithDatasetCreateRequestTaskChatCompletionEvaluationTaskRequest,
    EvaluationWithDatasetCreateRequestTaskGenericInferenceEvaluationTaskRequest,
    EvaluationWithDatasetCreateRequestTaskApplicationVariantV1EvaluationTaskRequest,
]

EvaluationCreateParams: TypeAlias = Union[
    EvaluationStandaloneCreateRequest, EvaluationFromDatasetCreateRequest, EvaluationWithDatasetCreateRequest
]
