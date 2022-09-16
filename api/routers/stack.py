from typing import List, Union, Optional

from fastapi import APIRouter, HTTPException, Header

import api.schemas.stack as schema
import api.cruds.stack as crud
from ..utils import get_user_info


router = APIRouter()


@router.get("/stacks", response_model=Union[List[schema.Stack], List[None]])
# async def read_stacks(user_id: int):
async def read_stacks(token: str = Header(default=None)):
    user_id = get_user_info(token)
    # from datetime import datetime
    # return [schema.Stack(userid=1, isbn=123, timestamp=datetime.now()), schema.Stack(userid=1, isbn=456, timestamp=datetime.now())]
    return await crud.read_all_stacks(user_id)


@router.post("/stack", response_model=schema.StackCreateResponse)
# async def create_stack(body: schema.StackCreate, token: Optional[str] = Header(default=None)):
async def create_stack(body: schema.StackCreate, token: str = Header(default=None)):
    user_id = get_user_info(token)
    print(user_id)
    # user_id = long(user_id)
    print(type(user_id))
    # from datetime import datetime
    # return schema.StackCreateResponse(user_id=user_id, **body.dict(), timestamp=datetime.now())
    return await crud.create_stack(user_id, body)
    
    
@router.delete("/stack", response_model=None)
async def delete_stack(body: schema.StackDelete):
    stack = await crud.read_stack(body)
    if stack is None:
        raise HTTPException(status_code=404, detail="Stack Not Found")
    # return None
    return await crud.delete_stack(body)
