# pyright: reportGeneralTypeIssues=false
from typing import Sequence

from toloka.a9s.client.models.generated.ai.toloka.a9s.webhooks.web.secret import (
    WebhookSignatureSecretFilterParamV1,
    WebhookSignatureSecretFormV1,
    WebhookSignatureSecretListViewV1,
    WebhookSignatureSecretViewV1,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.webhooks.web.secret_holder import (
    WebhookSignatureSecretHolderFilterParamV1,
    WebhookSignatureSecretHolderFormV1,
    WebhookSignatureSecretHolderListViewV1,
    WebhookSignatureSecretHolderViewV1,
)


class WebhookSignatureSecretFormStrict(WebhookSignatureSecretFormV1):
    pass


class WebhookSignatureSecretViewStrict(WebhookSignatureSecretViewV1):
    id: str
    created_at: str


class WebhookSignatureSecretFilterParamStrict(WebhookSignatureSecretFilterParamV1):
    pass


class WebhookSignatureSecretListViewStrict(WebhookSignatureSecretListViewV1):
    data: Sequence[WebhookSignatureSecretViewStrict]
    has_more: bool


class WebhookSignatureSecretHolderFormStrict(WebhookSignatureSecretHolderFormV1):
    pass


class WebhookSignatureSecretHolderViewStrict(WebhookSignatureSecretHolderViewV1):
    id: str
    created_at: str


class WebhookSignatureSecretHolderFilterParamStrict(WebhookSignatureSecretHolderFilterParamV1):
    pass


class WebhookSignatureSecretHolderListViewStrict(WebhookSignatureSecretHolderListViewV1):
    data: Sequence[WebhookSignatureSecretHolderViewStrict]
    has_more: bool
