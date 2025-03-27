from typing import AsyncGenerator

from toloka.a9s.client.base.client import AsyncBaseWebhooksClient
from toloka.a9s.client.base.converter import model_to_query_params
from toloka.a9s.client.client.webhook_secrets import (
    AsyncWebhookSignatureSecretClient,
    AsyncWebhookSignatureSecretHolderClient,
)
from toloka.a9s.client.models.utils import model_dump_a9s
from toloka.a9s.client.models.webhooks import (
    WebhookFilterParamStrict,
    WebhookFormStrict,
    WebhookListViewStrict,
    WebhookViewStrict,
)
from toloka.a9s.client.pagination import async_paginate
from toloka.a9s.client.sort import SortValue, from_sort_string, to_sort_string
from toloka.common.http.client import AsyncHttpClient


class AsyncWebhooksClient(AsyncBaseWebhooksClient):
    signature_secret: AsyncWebhookSignatureSecretClient
    signature_secret_holder: AsyncWebhookSignatureSecretHolderClient

    def __init__(self, transport: AsyncHttpClient) -> None:
        super().__init__(transport)
        self.signature_secret = AsyncWebhookSignatureSecretClient(transport)
        self.signature_secret_holder = AsyncWebhookSignatureSecretHolderClient(transport)

    async def create(self, form: WebhookFormStrict) -> WebhookViewStrict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/webhooks',
            body=model_dump_a9s(form),
        )
        return WebhookViewStrict.model_validate_json(response.text)

    async def get(self, webhook_id: str) -> WebhookViewStrict:
        response = await self.client.make_request(
            method='GET',
            url=f'{self.V1_PREFIX}/webhooks/{webhook_id}',
        )
        return WebhookViewStrict.model_validate_json(response.text)

    async def update(self, webhook_id: str, form: WebhookFormStrict) -> WebhookViewStrict:
        response = await self.client.make_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/webhooks/{webhook_id}',
            body=model_dump_a9s(form),
        )
        return WebhookViewStrict.model_validate_json(response.text)

    async def delete(self, webhook_id: str) -> None:
        await self.client.make_request(
            method='DELETE',
            url=f'{self.V1_PREFIX}/webhooks/{webhook_id}',
        )

    async def find(
        self,
        params: WebhookFilterParamStrict | None = None,
    ) -> WebhookListViewStrict:
        response = await self.client.make_request(
            method='GET',
            url=f'{self.V1_PREFIX}/webhooks',
            params=model_to_query_params(params) if params else None,
        )
        return WebhookListViewStrict.model_validate_json(response.text)

    async def get_all(
        self,
        params: WebhookFilterParamStrict | None = None,
    ) -> AsyncGenerator[WebhookViewStrict, None]:
        sort_criteria: dict[str, SortValue]
        if params is None or params.sort is None:
            sort_criteria = {'id': 'asc'}
        else:
            sort_criteria = from_sort_string(params.sort)
            sort_criteria['id'] = 'asc'

        async def get_next_page(page: WebhookListViewStrict | None) -> WebhookListViewStrict:
            last_id = max(webhook.id for webhook in page.data) if page else None
            params_copy = (
                params.model_copy(update={'sort': to_sort_string(sort_criteria), 'id_gt': last_id})
                if params
                else WebhookFilterParamStrict(sort=to_sort_string(sort_criteria), id_gt=last_id)
            )
            return await self.find(params_copy)

        webhook: WebhookViewStrict
        async for webhook in async_paginate(get_next_page=get_next_page):
            yield webhook
