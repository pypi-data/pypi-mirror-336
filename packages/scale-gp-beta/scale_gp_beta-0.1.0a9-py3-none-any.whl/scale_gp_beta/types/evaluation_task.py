# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "EvaluationTask",
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


class ChatCompletionEvaluationTaskConfiguration(BaseModel):
    messages: Union[List[Dict[str, object]], str]

    model: str

    audio: Union[Dict[str, object], str, None] = None

    frequency_penalty: Union[float, str, None] = None

    function_call: Union[Dict[str, object], str, None] = None

    functions: Union[List[Dict[str, object]], str, None] = None

    logit_bias: Union[Dict[str, int], str, None] = None

    logprobs: Union[bool, str, None] = None

    max_completion_tokens: Union[int, str, None] = None

    max_tokens: Union[int, str, None] = None

    metadata: Union[Dict[str, str], str, None] = None

    modalities: Union[List[str], str, None] = None

    n: Union[int, str, None] = None

    parallel_tool_calls: Union[bool, str, None] = None

    prediction: Union[Dict[str, object], str, None] = None

    presence_penalty: Union[float, str, None] = None

    reasoning_effort: Optional[str] = None

    response_format: Union[Dict[str, object], str, None] = None

    seed: Union[int, str, None] = None

    stop: Optional[str] = None

    store: Union[bool, str, None] = None

    temperature: Union[float, str, None] = None

    tool_choice: Optional[str] = None

    tools: Union[List[Dict[str, object]], str, None] = None

    top_k: Union[int, str, None] = None

    top_logprobs: Union[int, str, None] = None

    top_p: Union[float, str, None] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ChatCompletionEvaluationTask(BaseModel):
    configuration: ChatCompletionEvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Optional[Literal["chat_completion"]] = None


class GenericInferenceEvaluationTaskConfigurationInferenceConfigurationLaunchInferenceConfiguration(BaseModel):
    num_retries: Optional[int] = None

    timeout_seconds: Optional[int] = None


GenericInferenceEvaluationTaskConfigurationInferenceConfiguration: TypeAlias = Union[
    GenericInferenceEvaluationTaskConfigurationInferenceConfigurationLaunchInferenceConfiguration, str
]


class GenericInferenceEvaluationTaskConfiguration(BaseModel):
    model: str

    args: Union[Dict[str, object], str, None] = None

    inference_configuration: Optional[GenericInferenceEvaluationTaskConfigurationInferenceConfiguration] = None


class GenericInferenceEvaluationTask(BaseModel):
    configuration: GenericInferenceEvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Optional[Literal["inference"]] = None


class ApplicationVariantV1EvaluationTaskConfigurationHistoryUnionMember0(BaseModel):
    request: str
    """Request inputs"""

    response: str
    """Response outputs"""

    session_data: Optional[Dict[str, object]] = None
    """Session data corresponding to the request response pair"""


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState(BaseModel):
    current_node: str

    state: Dict[str, object]


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace(BaseModel):
    duration_ms: int

    node_id: str

    operation_input: str

    operation_output: str

    operation_type: str

    start_timestamp: str

    workflow_id: str

    operation_metadata: Optional[Dict[str, object]] = None


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides(BaseModel):
    concurrent: Optional[bool] = None

    initial_state: Optional[
        ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState
    ] = None

    partial_trace: Optional[
        List[ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace]
    ] = None

    use_channels: Optional[bool] = None


ApplicationVariantV1EvaluationTaskConfigurationOverrides: TypeAlias = Union[
    ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides, str
]


class ApplicationVariantV1EvaluationTaskConfiguration(BaseModel):
    application_variant_id: str

    inputs: Union[Dict[str, object], str]

    history: Union[List[ApplicationVariantV1EvaluationTaskConfigurationHistoryUnionMember0], str, None] = None

    operation_metadata: Union[Dict[str, object], str, None] = None

    overrides: Optional[ApplicationVariantV1EvaluationTaskConfigurationOverrides] = None
    """Execution override options for agentic applications"""


class ApplicationVariantV1EvaluationTask(BaseModel):
    configuration: ApplicationVariantV1EvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `task_type`"""

    task_type: Optional[Literal["application_variant"]] = None


EvaluationTask: TypeAlias = Annotated[
    Union[ChatCompletionEvaluationTask, GenericInferenceEvaluationTask, ApplicationVariantV1EvaluationTask],
    PropertyInfo(discriminator="task_type"),
]
