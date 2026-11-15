from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.get("", response_model=schemas.PaginatedResponse, summary="List semua kontak")
def list_contacts(
    page: int = Query(1, ge=1, description="Nomor halaman"),
    page_size: int = Query(20, ge=1, le=100, description="Jumlah data per halaman"),
    grup: str = Query(None, description="Filter berdasarkan grup (Keluarga, Teman, Kerja, dll)"),
    kota: str = Query(None, description="Filter berdasarkan kota"),
    is_favorite: bool = Query(None, description="Filter kontak favorit"),
    db: Session = Depends(get_db),
):
    total, data = crud.get_contacts(db, page=page, page_size=page_size, grup=grup, kota=kota, is_favorite=is_favorite)
    return {"total": total, "page": page, "page_size": page_size, "data": data}


@router.get("/search", response_model=schemas.PaginatedResponse, summary="Cari kontak")
def search_contacts(
    q: str = Query(..., min_length=1, description="Kata kunci pencarian (nama, email, no HP, kota, perusahaan)"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total, data = crud.search_contacts(db, q=q, page=page, page_size=page_size)
    return {"total": total, "page": page, "page_size": page_size, "data": data}


@router.get("/favorites", response_model=schemas.PaginatedResponse, summary="List kontak favorit")
def list_favorites(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total, data = crud.get_contacts(db, page=page, page_size=page_size, is_favorite=True)
    return {"total": total, "page": page, "page_size": page_size, "data": data}


@router.get("/{contact_id}", response_model=schemas.AddressBookOut, summary="Detail kontak")
def get_contact(contact_id: UUID, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Kontak tidak ditemukan")
    return contact


@router.post("", response_model=schemas.AddressBookOut, status_code=201, summary="Tambah kontak baru")
def create_contact(payload: schemas.AddressBookCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, payload)


@router.put("/{contact_id}", response_model=schemas.AddressBookOut, summary="Update kontak")
def update_contact(contact_id: UUID, payload: schemas.AddressBookUpdate, db: Session = Depends(get_db)):
    contact = crud.update_contact(db, contact_id, payload)
    if not contact:
        raise HTTPException(status_code=404, detail="Kontak tidak ditemukan")
    return contact


@router.delete("/{contact_id}", status_code=204, summary="Hapus kontak")
def delete_contact(contact_id: UUID, db: Session = Depends(get_db)):
    deleted = crud.delete_contact(db, contact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Kontak tidak ditemukan")
