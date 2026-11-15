from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/ref", tags=["Referensi"])


@router.get("/agama", response_model=list[schemas.RefAgamaOut], summary="List referensi agama")
def list_agama(db: Session = Depends(get_db)):
    return crud.get_ref_agama(db)


@router.get("/status-perkawinan", response_model=list[schemas.RefStatusPerkawinanOut], summary="List referensi status perkawinan")
def list_status_perkawinan(db: Session = Depends(get_db)):
    return crud.get_ref_status_perkawinan(db)


@router.get("/jenis-kelamin", response_model=list[schemas.RefJenisKelaminOut], summary="List referensi jenis kelamin")
def list_jenis_kelamin(db: Session = Depends(get_db)):
    return crud.get_ref_jenis_kelamin(db)
