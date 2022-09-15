from typing import List, Union, Optional

from fastapi import APIRouter, HTTPException, Header

import api.schemas.user as schema
import api.cruds.user as crud


router = APIRouter()


# @router.get("/users", response_model=Union[List[schema.User], List[None]])
@router.get("/users")
async def read_all_users(authorization: Optional[str] = Header(default=None)):
    from auth0.v3.authentication import Users
    import os
    domain = os.getenv("DOMAIN")
    users = Users(domain)
    print(users)
    myuser = users.userinfo(authorization)
    print(myuser.keys())
    return {"a": myuser["sub"]}
    # return [schema.User(userid=1, name='name1'), schema.User(userid=2, name='name2')]
    return await crud.read_all_users()


@router.get("/user", response_model=schema.User)
async def read_user(user_id: int):
    # return User(userid=user_id, name='name')
    return await crud.read_user(user_id)


@router.post("/user", response_model=schema.UserCreateResponse)
async def create_user(body: schema.UserCreate):
    # return schema.UserCreateResponse(userid=1, **body.dict())
    return await crud.create_user(body)
    

@router.put("/user", response_model=schema.UserCreateResponse)
async def update_user(user_id: int, body: schema.UserCreate):
    user = await crud.read_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    # return schema.UserCreateResponse(userid=user_id, **body.dict())
    return await crud.update_user(user_id, body)
    
    
@router.delete("/user", response_model=None)
async def delete_user(user_id: int):
    user = await crud.read_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    # return await None
    return await crud.delete_user(user_id)
