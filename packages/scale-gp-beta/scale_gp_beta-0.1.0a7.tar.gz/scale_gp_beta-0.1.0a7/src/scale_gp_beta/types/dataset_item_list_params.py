# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["DatasetItemListParams"]


class DatasetItemListParams(TypedDict, total=False):
    dataset_id: Optional[str]
    """Optional dataset identifier.

    Must be provided if a specific version is requested.
    """

    ending_before: Optional[str]

    include_archived: bool

    limit: int

    starting_after: Optional[str]

    version: Optional[int]
    """Optional dataset version.

    When unset, returns the latest version. Requires a valid dataset_id when set.
    """
