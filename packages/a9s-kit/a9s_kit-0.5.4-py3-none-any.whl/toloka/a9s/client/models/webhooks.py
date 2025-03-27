# pyright: reportGeneralTypeIssues=false
from datetime import datetime
from typing import Literal, Sequence

from pydantic import BaseModel

from toloka.a9s.client.models.generated.ai.toloka.a9s.webhooks.web import (
    WebhookFilterParamV1,
    WebhookFormV1,
    WebhookListViewV1,
    WebhookViewV1,
)
from toloka.a9s.client.models.types import (
    AnnotationGroupId,
    AnnotationId,
    AnnotationProcessId,
    BatchId,
    ProjectId,
)


class StatusWorkflowStatusChangedParams(BaseModel):
    status_workflow_status_changed_statuses: Sequence[str]


WebhookActionParams = StatusWorkflowStatusChangedParams


class WebhookFormStrict(WebhookFormV1):
    action_params: WebhookActionParams | None = None


class WebhookViewStrict(WebhookViewV1):
    id: str
    created_at: str
    action_params: WebhookActionParams | None = None


class WebhookFilterParamStrict(WebhookFilterParamV1):
    pass


class WebhookListViewStrict(WebhookListViewV1):
    data: Sequence[WebhookViewStrict]
    has_more: bool


class BaseWebhookEvent(BaseModel):
    event_id: str
    webhook_id: str
    current_request_timestamp: datetime


class QuorumCompletedPayload(BaseModel):
    annotation_process_id: AnnotationProcessId
    created_at: datetime
    modified_at: datetime
    project_id: ProjectId
    batch_id: BatchId
    annotation_group_id: AnnotationGroupId


class StatusWorkflowStatusChangedPayload(BaseModel):
    annotation_process_id: AnnotationProcessId
    created_at: datetime
    modified_at: datetime
    project_id: ProjectId
    batch_id: BatchId
    annotation_group_id: AnnotationGroupId
    annotation_id: AnnotationId
    status: str
    counter: int


class QuorumCompletedEvent(BaseWebhookEvent):
    action: Literal['QUORUM_COMPLETED'] = 'QUORUM_COMPLETED'
    payload: QuorumCompletedPayload


class StatusWorkflowStatusChangedEvent(BaseWebhookEvent):
    action: Literal['STATUS_WORKFLOW_STATUS_CHANGED'] = 'STATUS_WORKFLOW_STATUS_CHANGED'
    payload: StatusWorkflowStatusChangedPayload


WebhookEvent = QuorumCompletedEvent | StatusWorkflowStatusChangedEvent
