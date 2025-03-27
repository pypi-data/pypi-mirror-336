# pyright: reportGeneralTypeIssues=false

from typing import Annotated, Literal, Sequence

from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.reset.web.v0.view import (
    ResetListViewV0,
    ResetViewV0,
)
from toloka.a9s.client.models.types import ResetId
from toloka.a9s.client.models.utils import none_default_validator


class ResetViewV0Strict(ResetViewV0):
    id: ResetId
    quality_config_id: str
    quality_config_type: Literal['SYNC', 'ASYNC']
    account_id: str
    rule_name: str
    reset_time: str


class ResetListViewV0Strict(ResetListViewV0):
    data: Annotated[Sequence[ResetViewV0Strict], none_default_validator(default_factory=list)]
