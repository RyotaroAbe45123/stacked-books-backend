from typing import List, Union

from fastapi import APIRouter, HTTPException

import api.schemas.stack as schema
import api.cruds.stack as crud


router = APIRouter()


@router.get("/stacks", response_model=Union[List[schema.Stack], List[None]])
async def read_stacks(user_id: int):
    # from datetime import datetime
    # return [schema.Stack(userid=1, isbn=123, timestamp=datetime.now()), schema.Stack(userid=1, isbn=456, timestamp=datetime.now())]
    return await crud.read_all_stacks(user_id)


@router.post("/stack", response_model=schema.StackCreateResponse)
async def create_stack(body: schema.StackCreate):
    # from datetime import datetime
    # return schema.StackCreateResponse(**body.dict(), timestamp=datetime.now())
    return await crud.create_stack(body)
    
    
@router.delete("/stack", response_model=None)
async def delete_stack(body: schema.StackDelete):
    stack = await crud.read_stack(body)
    if stack is None:
        raise HTTPException(status_code=404, detail="Stack Not Found")
    # return None
    return await crud.delete_stack(body)
