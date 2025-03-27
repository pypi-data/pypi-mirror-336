from typing import List, Optional
from gestell.types import BaseRequest, BaseResponse, Job, JobStatusType
import aiohttp


class GetJobsRequest(BaseRequest):
    collection_id: str
    take: Optional[int] = 10
    skip: Optional[int] = 0
    status: Optional[JobStatusType] = 'all'
    nodes: Optional[JobStatusType] = 'all'
    edges: Optional[JobStatusType] = 'all'
    vectors: Optional[JobStatusType] = 'all'
    category: Optional[JobStatusType] = 'all'


class GetJobsResponse(BaseResponse):
    result: List[Job]


async def list_jobs(request: GetJobsRequest) -> GetJobsResponse:
    url = f'{request.api_url}/api/collection/{request.collection_id}/job'

    params = {
        'take': request.take,
        'skip': request.skip,
        'status': request.status,
        'nodes': request.nodes,
        'edges': request.edges,
        'vectors': request.vectors,
        'category': request.category,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url,
                headers={'Authorization': f'BEARER {request.api_key}'},
                params=params,
            ) as response:
                if not response.ok:
                    error_response = await response.json()
                    if request.debug:
                        print(error_response)
                    return GetJobsResponse(
                        status='ERROR',
                        message=error_response.get(
                            'message', 'There was an error retrieving jobs'
                        ),
                        result=[],
                    )

                response_data = await response.json()
                return GetJobsResponse(**response_data)
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            return GetJobsResponse(
                status='ERROR',
                message=f'An error occurred during the request: {e}',
                result=[],
            )
