from typing import AsyncGenerator

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient, AsyncBaseWebhooksClient
from toloka.a9s.client.base.converter import model_to_query_params
from toloka.a9s.client.models.generated.ai.toloka.a9s.project.web.v1.form import (
    GetProjectListQueryParamsV1,
    ProjectFormV1,
)
from toloka.a9s.client.models.project import ListProjectViewV1Strict, ProjectViewV1Strict
from toloka.a9s.client.models.utils import model_dump_a9s
from toloka.a9s.client.models.webhook_secrets import (
    WebhookSignatureSecretFilterParamStrict,
    WebhookSignatureSecretFormStrict,
    WebhookSignatureSecretHolderFilterParamStrict,
    WebhookSignatureSecretHolderFormStrict,
    WebhookSignatureSecretHolderListViewStrict,
    WebhookSignatureSecretHolderViewStrict,
    WebhookSignatureSecretListViewStrict,
    WebhookSignatureSecretViewStrict,
)
from toloka.a9s.client.pagination import async_paginate
from toloka.a9s.client.sort import SortValue, from_sort_string, to_sort_string


class AsyncAnnotationStudioProjectsClient(AsyncBaseAnnotationStudioClient):
    async def create(self, form: ProjectFormV1) -> ProjectViewV1Strict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/projects',
            body=model_dump_a9s(form),
        )
        return ProjectViewV1Strict.model_validate(response.json())

    async def get(self, project_id: str) -> ProjectViewV1Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V1_PREFIX}/projects/{project_id}',
        )
        return ProjectViewV1Strict.model_validate(response.json())

    async def update(self, project_id: str, form: ProjectFormV1) -> ProjectViewV1Strict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/projects/{project_id}',
            body=model_dump_a9s(form),
        )
        return ProjectViewV1Strict.model_validate(response.json())

    async def find(self, query_params: GetProjectListQueryParamsV1) -> ListProjectViewV1Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V1_PREFIX}/projects',
            params=model_to_query_params(query_params),
        )
        return ListProjectViewV1Strict.model_validate(response.json())

    async def get_all(self, query_params: GetProjectListQueryParamsV1) -> AsyncGenerator[ProjectViewV1Strict, None]:
        sort_criteria: dict[str, SortValue]
        if query_params.sort is None:
            sort_criteria = {'id': 'asc'}
        else:
            sort_criteria = from_sort_string(query_params.sort)
            sort_criteria['id'] = 'asc'

        async def get_next_page(page: ListProjectViewV1Strict | None) -> ListProjectViewV1Strict:
            last_id = max(project.id for project in page.data) if page else None
            return await self.find(
                query_params.model_copy(update={'sort': to_sort_string(sort_criteria), 'id_gt': last_id})
            )

        project: ProjectViewV1Strict
        async for project in async_paginate(get_next_page=get_next_page):
            yield project


class AsyncWebhookSignatureSecretClient(AsyncBaseWebhooksClient):
    async def create(self, form: WebhookSignatureSecretFormStrict) -> WebhookSignatureSecretViewStrict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/webhooks/signature-secrets',
            body=model_dump_a9s(form),
        )
        return WebhookSignatureSecretViewStrict.model_validate(response.json())

    async def get(self, secret_id: str) -> WebhookSignatureSecretViewStrict:
        response = await self.client.make_request(
            method='GET',
            url=f'{self.V1_PREFIX}/webhooks/signature-secrets/{secret_id}',
        )
        return WebhookSignatureSecretViewStrict.model_validate(response.json())

    async def update(self, secret_id: str, form: WebhookSignatureSecretFormStrict) -> WebhookSignatureSecretViewStrict:
        response = await self.client.make_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/webhooks/signature-secrets/{secret_id}',
            body=model_dump_a9s(form),
        )
        return WebhookSignatureSecretViewStrict.model_validate(response.json())

    async def delete(self, secret_id: str) -> None:
        await self.client.make_request(
            method='DELETE',
            url=f'{self.V1_PREFIX}/webhooks/signature-secrets/{secret_id}',
        )

    async def find(
        self,
        params: WebhookSignatureSecretFilterParamStrict | None = None,
    ) -> WebhookSignatureSecretListViewStrict:
        response = await self.client.make_request(
            method='GET',
            url=f'{self.V1_PREFIX}/webhooks/signature-secrets',
            params=model_to_query_params(params) if params else None,
        )
        return WebhookSignatureSecretListViewStrict.model_validate(response.json())

    async def get_all(
        self,
        params: WebhookSignatureSecretFilterParamStrict | None = None,
    ) -> AsyncGenerator[WebhookSignatureSecretViewStrict, None]:
        sort_criteria: dict[str, SortValue]
        if params is None or params.sort is None:
            sort_criteria = {'id': 'asc'}
        else:
            sort_criteria = from_sort_string(params.sort)
            sort_criteria['id'] = 'asc'

        async def get_next_page(
            page: WebhookSignatureSecretListViewStrict | None,
        ) -> WebhookSignatureSecretListViewStrict:
            last_id = max(secret.id for secret in page.data) if page else None
            params_copy = (
                params.model_copy(update={'sort': to_sort_string(sort_criteria), 'id_gt': last_id})
                if params
                else WebhookSignatureSecretFilterParamStrict(sort=to_sort_string(sort_criteria), id_gt=last_id)
            )
            return await self.find(params_copy)

        secret: WebhookSignatureSecretViewStrict
        async for secret in async_paginate(get_next_page=get_next_page):
            yield secret


class AsyncWebhookSignatureSecretHolderClient(AsyncBaseWebhooksClient):
    async def create(self, form: WebhookSignatureSecretHolderFormStrict) -> WebhookSignatureSecretHolderViewStrict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/webhooks/signature-secret-holders',
            body=model_dump_a9s(form),
        )
        return WebhookSignatureSecretHolderViewStrict.model_validate(response.json())

    async def get(self, holder_id: str) -> WebhookSignatureSecretHolderViewStrict:
        response = await self.client.make_request(
            method='GET',
            url=f'{self.V1_PREFIX}/webhooks/signature-secret-holders/{holder_id}',
        )
        return WebhookSignatureSecretHolderViewStrict.model_validate(response.json())

    async def update(
        self, holder_id: str, form: WebhookSignatureSecretHolderFormStrict
    ) -> WebhookSignatureSecretHolderViewStrict:
        response = await self.client.make_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/webhooks/signature-secret-holders/{holder_id}',
            body=model_dump_a9s(form),
        )
        return WebhookSignatureSecretHolderViewStrict.model_validate(response.json())

    async def delete(self, holder_id: str) -> None:
        await self.client.make_request(
            method='DELETE',
            url=f'{self.V1_PREFIX}/webhooks/signature-secret-holders/{holder_id}',
        )

    async def find(
        self,
        params: WebhookSignatureSecretHolderFilterParamStrict | None = None,
    ) -> WebhookSignatureSecretHolderListViewStrict:
        response = await self.client.make_request(
            method='GET',
            url=f'{self.V1_PREFIX}/webhooks/signature-secret-holders',
            params=model_to_query_params(params) if params else None,
        )
        return WebhookSignatureSecretHolderListViewStrict.model_validate(response.json())

    async def get_all(
        self,
        params: WebhookSignatureSecretHolderFilterParamStrict | None = None,
    ) -> AsyncGenerator[WebhookSignatureSecretHolderViewStrict, None]:
        sort_criteria: dict[str, SortValue]
        if params is None or params.sort is None:
            sort_criteria = {'id': 'asc'}
        else:
            sort_criteria = from_sort_string(params.sort)
            sort_criteria['id'] = 'asc'

        async def get_next_page(
            page: WebhookSignatureSecretHolderListViewStrict | None,
        ) -> WebhookSignatureSecretHolderListViewStrict:
            last_id = max(holder.id for holder in page.data) if page else None
            params_copy = (
                params.model_copy(update={'sort': to_sort_string(sort_criteria), 'id_gt': last_id})
                if params
                else WebhookSignatureSecretHolderFilterParamStrict(sort=to_sort_string(sort_criteria), id_gt=last_id)
            )
            return await self.find(params_copy)

        holder: WebhookSignatureSecretHolderViewStrict
        async for holder in async_paginate(get_next_page=get_next_page):
            yield holder
