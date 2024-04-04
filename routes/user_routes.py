from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from bson.objectid import ObjectId

from backend.models.user_model import UserModel
from backend.controllers.user_controller import (register, login, update_user_byID, delete_user_byID,
                                                 delete_all_users_db)


def get_user_router(users_collection, tokens_collection):
    router = APIRouter()

    @router.post("/register", tags=["auth"])
    async def register_route(data_user: UserModel):
        result = await register(data_user, users_collection)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result

    @router.post("/login", tags=["auth"])
    async def login_route(form_data: OAuth2PasswordRequestForm = Depends()):
        result = await login(users_collection, tokens_collection, form_data)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result

    @router.delete("/rm", response_model=dict)
    async def delete_all_users(token: str = Header(None)):
        result = await delete_all_users_db(token, users_collection)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result

    @router.delete("/{user_id}", response_model=dict)
    async def delete_user(user_id: str, token: str = Header(None)):
        result = await delete_user_byID(user_id, token, users_collection)
        if "error" in result:
            raise HTTPException(status_code=403, detail=result["error"])
        return result

    return router
