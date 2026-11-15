from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app import models, schemas
from app.database import get_db
from app.security import verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    user: schemas.UserOut


@router.post("/login", response_model=LoginResponse, summary="Login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.AppUser).filter(
        models.AppUser.username == payload.username
    ).first()

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Username atau password salah")

    if not user.aktif:
        raise HTTPException(status_code=403, detail="Akun Anda tidak aktif")

    return {"message": "Login berhasil", "user": user}
