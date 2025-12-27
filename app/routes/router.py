from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.schema.login import UserLogin, UserSignup
from app.services.auth import authenticate_user, register_new_user,get_all_users
from app.config.db import get_db  # Import your database session

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login")
async def login(
    user: UserLogin = Body(..., description="User login credentials"),
    db: Session = Depends(get_db)
):
    try:
        # Make sure authenticate_user is updated to accept db as parameter
        result = authenticate_user(db, user.username, user.password)
        if not result:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"message": "Login successful", "user": result}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/signup")
async def signup(user: UserSignup, db: Session = Depends(get_db)):
    try:
        result = register_new_user(
            db=db,
            email=user.email,
            firstname=user.firstname,
            lastname=user.lastname,
            password=user.password,
            phone=user.phone,
            dob=user.dob
        )
        return {
            "message": "Signup successful",
            "user_id": result.id,
            "email": user.email
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during signup")
@router.get("/all_users")
async def get_users_endpoint(db: Session = Depends(get_db),skip: int = 0, limit: int = 100):
    try:
        users = get_all_users(db,skip=skip, limit=limit)
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching users")