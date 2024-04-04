from bson import ObjectId
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError, OperationFailure, PyMongoError
from backend.auth.jwt_manager import Token
from backend.interfaces.token_interface import TokenInterface
from backend.interfaces.user_interface import UserInterface
from backend.models.user_model import UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register(data_user: UserModel, users_collection: Collection):
    try:
        existing_user = UserInterface.get_user(collection=users_collection, email=data_user.email)
        if existing_user:
            return {"error": "A user with this email already exists"}

        hashed_password = pwd_context.hash(data_user.password)
        user_dict = data_user.dict()
        user_dict["hashed_password"] = hashed_password

        if user_dict["timestamp"] is not None:
            user_dict["timestamp"] = user_dict["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

        result = UserInterface.add_user(collection=users_collection, user=user_dict)
        return {"message": "User created", "id": str(result.inserted_id)}
    except DuplicateKeyError:
        return {"error": "Username already exists"}
    except OperationFailure as e:
        return {"error": str(e)}
    except PyMongoError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


async def login(users_collection: Collection, tokens_collection: Collection,
                form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = UserInterface.get_user(collection=users_collection, email=form_data.username)
        if not user:
            return {"error": "E-mail not found"}
        if not pwd_context.verify(form_data.password, user["hashed_password"]):
            return {"error": "Incorrect password"}
        token: str = Token.create_token(data={"access": user["email"]})
        TokenInterface.add_token(collection=tokens_collection, token={"token": token, "email": user["email"]})
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


async def update_user_byID(user_id: str, updated_data: UserModel, token: str, users_collection: Collection):
    try:
        email = Token.verify_token(token=token)
        user = UserInterface.get_user(collection=users_collection, email=email)
        if not user:
            return {"error": "User not found"}
        updated_data_dict = updated_data.dict()

        if updated_data_dict["timestamp"] is not None:
            updated_data_dict["timestamp"] = updated_data_dict["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

        user_id = ObjectId(user_id)
        result = UserInterface.update_user(collection=users_collection, user_id=user_id, updated_data=updated_data_dict)
        if result.modified_count == 1:
            return {"message": "User updated successfully"}
        else:
            return {"error": f"Record not found to update with ID: {user_id}"}
    except HTTPException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


async def delete_user_byID(user_id: str, token: str, users_collection: Collection):
    try:
        if token is None:
            return {"error": "Token is missing"}

        email = Token.verify_token(token=token)
        if email is None:
            return {"error": "Invalid token"}
        user = UserInterface.get_user(collection=users_collection, email=email)
        if not user:
            return {"error": "User not found"}

        user_id = ObjectId(user_id)
        UserInterface.delete_user(collection=users_collection, user_id=user_id)
        return {"message": "User deleted"}
    except HTTPException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


async def delete_all_users_db(token: str, users_collection: Collection):
    try:
        email = Token.verify_token(token=token)
        user = UserInterface.get_user(collection=users_collection, email=email)
        if not user:
            return {"error": "Invalid access token"}
        UserInterface.delete_all_users(collection=users_collection)
        return {"message": "All users deleted"}
    except HTTPException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
