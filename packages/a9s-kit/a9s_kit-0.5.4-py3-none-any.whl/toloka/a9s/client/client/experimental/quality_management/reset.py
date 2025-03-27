from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.base.converter import model_to_query_params
from toloka.a9s.client.models.generated.ai.toloka.a9s.qms.reset.web.v0.form import (
    GetResetListQueryParamsV0,
    ResetFormV0,
)
from toloka.a9s.client.models.quality_management.reset import (
    ResetListViewV0Strict,
    ResetViewV0Strict,
)


class AsyncQmsResetClient(AsyncBaseAnnotationStudioClient):
    API_PREFIX = f'{AsyncBaseAnnotationStudioClient.V0_PREFIX}/resets'

    async def get(self, id: str) -> ResetViewV0Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.API_PREFIX}/{id}',
        )
        return ResetViewV0Strict.model_validate(response.json())

    async def create(self, form: ResetFormV0) -> ResetViewV0Strict:
        response = await self.client.make_request(
            method='POST',
            url=self.API_PREFIX,
            body=form.model_dump(mode='json'),
        )
        return ResetViewV0Strict.model_validate(response.json())

    async def update(self, id: str, form: ResetFormV0) -> ResetViewV0Strict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.API_PREFIX}/{id}',
            body=form.model_dump(mode='json'),
        )
        return ResetViewV0Strict.model_validate(response.json())

    async def delete(self, id: str) -> None:
        await self.client.make_retriable_request(
            method='DELETE',
            url=f'{self.API_PREFIX}/{id}',
        )

    async def find(self, query_params: GetResetListQueryParamsV0) -> ResetListViewV0Strict:
        response = await self.client.make_retriable_request(
            method='GET',
            url=self.API_PREFIX,
            params=model_to_query_params(query_params),
        )
        return ResetListViewV0Strict.model_validate(response.json())
