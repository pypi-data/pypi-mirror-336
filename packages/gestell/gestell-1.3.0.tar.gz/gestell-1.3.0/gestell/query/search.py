import json
from typing import List
from gestell.types import BaseRequest, BaseResponse, QueryPayload, SearchResult, QueryKV
import aiohttp


class SearchQueryRequest(BaseRequest, QueryPayload):
    pass


class SearchQueryResponse(BaseResponse):
    result: List[SearchResult]


async def search_query(request: SearchQueryRequest) -> SearchQueryResponse:
    url = f'{request.api_url}/api/collection/{request.collection_id}/search'

    payload = {
        'categoryId': request.category_id,
        'prompt': request.prompt,
        'method': request.method or 'normal',
        'type': request.type or QueryKV[request.method or 'normal'].type,
        'vectorDepth': request.vectorDepth
        or QueryKV[request.method or 'normal'].vectorDepth,
        'nodeDepth': request.nodeDepth or QueryKV[request.method or 'normal'].nodeDepth,
        'maxQueries': request.maxQueries
        or QueryKV[request.method or 'normal'].maxQueries,
        'maxResults': request.maxResults
        or QueryKV[request.method or 'normal'].maxResults,
        'includeContent': request.includeContent
        if request.includeContent is not None
        else True,
        'includeEdges': request.includeEdges
        if request.includeEdges is not None
        else False,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
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
                    return SearchQueryResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error running the search query'
                        ),
                        result=[],
                    )

                response_data = await response.json()
                return SearchQueryResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return SearchQueryResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                result=[],
            )
