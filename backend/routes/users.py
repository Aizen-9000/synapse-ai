from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import UserCreate, UserOut, Token
from ..auth import hash_password, verify_password, create_access_token
from ..db import users_collection

router = APIRouter(prefix="/users")

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate):
    existing = await users_collection.find_one({"email": user_in.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user_in.password)
    user_doc = {"email": user_in.email, "hashed_password": hashed, "is_premium": False, "is_active": True}
    res = await users_collection.insert_one(user_doc)
    user_doc["id"] = str(res.inserted_id)
    return {"id": user_doc["id"], "email": user_doc["email"], "is_premium": user_doc["is_premium"]}

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(str(user["_id"]))
    return {"access_token": token, "token_type": "bearer"}