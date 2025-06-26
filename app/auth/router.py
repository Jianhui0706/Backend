from fastapi import APIRouter, HTTPException
from app.auth.auth import UserCreate
from app.auth.utils import hash_password
from app.database import user_collection
import traceback

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user: UserCreate):
    try:
        # check if email have alr been registered
        if user_collection.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="Email already registered")

        # check if username is alr taken
        if user_collection.find_one({"username": user.username}):
            raise HTTPException(status_code=400, detail="Username already taken")

        # hashes the password
        hashed_pw = hash_password(user.password)
        user_collection.insert_one({
            "email": user.email,
            "username": user.username,
            "password": hashed_pw,
            "vehicle": None
        })
        return {"msg": "User registered successfully"}

    # FastAPI handles sending error 400 bad request, 
    # for handling email/username already taken
    except HTTPException as e:
        raise e
    
    except Exception as e:
        print("Error in /register:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")

# used to print list of successfully registered user details (excl password)
# accessed through: http://localhost:8000/auth/users
@router.get("/users")
def get_users():
    users = list(user_collection.find({}, {"_id": 0, "password": 0}))
    return users