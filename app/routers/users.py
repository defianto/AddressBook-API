from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.security import hash_password, verify_password

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_or_404(user_id: int, db: Session) -> models.AppUser:
    user = db.query(models.AppUser).filter(models.AppUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return user


# ── GET /users ─────────────────────────────────────────────────────────────────

@router.get("", response_model=list[schemas.UserOut], summary="List semua user")
def list_users(
    aktif: bool = Query(None, description="Filter berdasarkan status aktif"),
    role: str = Query(None, description="Filter berdasarkan role (ADMIN/USER)"),
    db: Session = Depends(get_db),
):
    query = db.query(models.AppUser)
    if aktif is not None:
        query = query.filter(models.AppUser.aktif == aktif)
    if role:
        query = query.filter(models.AppUser.role == role.upper())
    return query.order_by(models.AppUser.nama_lengkap).all()


# ── GET /users/{id} ────────────────────────────────────────────────────────────

@router.get("/{user_id}", response_model=schemas.UserOut, summary="Detail user")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_or_404(user_id, db)


# ── POST /users ────────────────────────────────────────────────────────────────

@router.post("", response_model=schemas.UserOut, status_code=201, summary="Tambah user baru")
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    # Cek username sudah ada
    existing = db.query(models.AppUser).filter(models.AppUser.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username sudah digunakan")

    user = models.AppUser(
        username=payload.username,
        password=hash_password(payload.password),
        nama_lengkap=payload.nama_lengkap,
        email=payload.email,
        role=payload.role.upper() if payload.role else "USER",
        aktif=payload.aktif if payload.aktif is not None else True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ── PUT /users/{id} ────────────────────────────────────────────────────────────

@router.put("/{user_id}", response_model=schemas.UserOut, summary="Edit user")
def update_user(user_id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = get_user_or_404(user_id, db)
    update_data = payload.model_dump(exclude_unset=True)
    if "role" in update_data and update_data["role"]:
        update_data["role"] = update_data["role"].upper()
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


# ── POST /users/{id}/change-password ──────────────────────────────────────────

@router.post("/{user_id}/change-password", summary="Ganti password")
def change_password(user_id: int, payload: schemas.UserChangePassword, db: Session = Depends(get_db)):
    user = get_user_or_404(user_id, db)

    if not verify_password(payload.password_lama, user.password):
        raise HTTPException(status_code=400, detail="Password lama tidak cocok")

    user.password = hash_password(payload.password_baru)
    db.commit()
    return {"message": "Password berhasil diubah"}


# ── POST /users/{id}/toggle-aktif ─────────────────────────────────────────────

@router.post("/{user_id}/toggle-aktif", response_model=schemas.UserOut, summary="Aktifkan / nonaktifkan user")
def toggle_aktif(user_id: int, db: Session = Depends(get_db)):
    user = get_user_or_404(user_id, db)
    user.aktif = not user.aktif
    db.commit()
    db.refresh(user)
    return user


# ── DELETE /users/{id} ────────────────────────────────────────────────────────

@router.delete("/{user_id}", status_code=204, summary="Hapus user")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_or_404(user_id, db)
    db.delete(user)
    db.commit()
