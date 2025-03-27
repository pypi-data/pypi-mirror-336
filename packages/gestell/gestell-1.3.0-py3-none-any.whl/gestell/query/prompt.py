import json
from typing import AsyncGenerator, Dict, Literal, Optional
from gestell.types import BaseRequest, PromptPayload, QueryKV
import aiohttp


PromptMessage = Dict[Literal['role', 'content'], str]


class PromptQueryRequest(BaseRequest, PromptPayload):
    category_id: Optional[str]
    prompt: str
    method: Optional[str]
    type: Optional[str]
    vectorDepth: Optional[int]
    nodeDepth: Optional[int]
    maxQueries: Optional[int]
    maxResults: Optional[int]
    template: Optional[str]
    cot: Optional[bool]
    messages: Optional[list[PromptMessage]]


async def prompt_query(
    request: PromptQueryRequest,
) -> AsyncGenerator[bytes, None]:
    url = f'{request.api_url}/api/collection/{request.collection_id}/prompt'

    payload = {
        'categoryId': request.category_id,
        'prompt': request.prompt,
        'method': request.method,
        'type': request.type or QueryKV[request.method].type
        if request.method
        else None,
        'vectorDepth': request.vectorDepth or QueryKV[request.method].vectorDepth
        if request.method
        else None,
        'nodeDepth': request.nodeDepth or QueryKV[request.method].nodeDepth
        if request.method
        else None,
        'maxQueries': request.maxQueries or QueryKV[request.method].maxQueries
        if request.method
        else None,
        'maxResults': request.maxResults or QueryKV[request.method].maxResults
        if request.method
        else None,
        'template': request.template,
        'cot': request.cot,
        'threadId': request.threadId,
        'chat': request.chat,
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
            ) as r:
                async for chunk in r.content:
                    yield chunk
        except aiohttp.ClientError as e:
            if request.debug:
                print(f'Client Error: {e}')
            raise e
