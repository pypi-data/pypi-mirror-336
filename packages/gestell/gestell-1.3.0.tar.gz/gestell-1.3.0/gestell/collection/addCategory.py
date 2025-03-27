import json
from gestell.types import BaseRequest, BaseResponse, CategoryType
import aiohttp


class AddCategoryRequest(BaseRequest):
    collection_id: str
    name: str
    type: CategoryType
    instructions: str


class AddCategoryResponse(BaseResponse):
    id: str


async def add_category(
    request: AddCategoryRequest,
) -> AddCategoryResponse:
    url = f'{request.api_url}/api/collection/{request.collection_id}/category'

    payload = {
        'name': request.name,
        'type': request.type,
        'instructions': request.instructions,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.put(
                url,
                headers={
                    'Authorization': f'BEARER {request.api_key}',
                    'Content-Type': 'application/json',
                },
                data=json.dumps(payload),
            ) as response:
                if not response.ok:
                    error_response = await response.json()
                    if request.debug:
                        print(error_response)
                    return AddCategoryResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error creating a category'
                        ),
                        id='',
                    )

                response_data = await response.json()
                return AddCategoryResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return AddCategoryResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                id='',
            )
