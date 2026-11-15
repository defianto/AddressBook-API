from sqlalchemy.orm import Session
from sqlalchemy import or_
from uuid import UUID
from app import models, schemas


# ── READ: List dengan pagination & filter ──────────────────────────────────────

def get_contacts(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    grup: str = None,
    kota: str = None,
    is_favorite: bool = None,
):
    query = db.query(models.AddressBook)

    if grup:
        query = query.filter(models.AddressBook.grup == grup)
    if kota:
        query = query.filter(models.AddressBook.kota.ilike(f"%{kota}%"))
    if is_favorite is not None:
        query = query.filter(models.AddressBook.is_favorite == is_favorite)

    total = query.count()
    data = query.order_by(models.AddressBook.nama).offset((page - 1) * page_size).limit(page_size).all()
    return total, data


# ── READ: Detail satu kontak ───────────────────────────────────────────────────

def get_contact(db: Session, contact_id: UUID):
    return db.query(models.AddressBook).filter(models.AddressBook.id == contact_id).first()


# ── READ: Search ───────────────────────────────────────────────────────────────

def search_contacts(db: Session, q: str, page: int = 1, page_size: int = 20):
    keyword = f"%{q}%"
    query = db.query(models.AddressBook).filter(
        or_(
            models.AddressBook.nama.ilike(keyword),
            models.AddressBook.nama_lengkap.ilike(keyword),
            models.AddressBook.nama_alias.ilike(keyword),
            models.AddressBook.email.ilike(keyword),
            models.AddressBook.no_hp.ilike(keyword),
            models.AddressBook.no_wa.ilike(keyword),
            models.AddressBook.perusahaan.ilike(keyword),
            models.AddressBook.kota.ilike(keyword),
        )
    )
    total = query.count()
    data = query.order_by(models.AddressBook.nama).offset((page - 1) * page_size).limit(page_size).all()
    return total, data


# ── CREATE ─────────────────────────────────────────────────────────────────────

def create_contact(db: Session, payload: schemas.AddressBookCreate):
    contact = models.AddressBook(**payload.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


# ── UPDATE ─────────────────────────────────────────────────────────────────────

def update_contact(db: Session, contact_id: UUID, payload: schemas.AddressBookUpdate):
    contact = get_contact(db, contact_id)
    if not contact:
        return None
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


# ── DELETE ─────────────────────────────────────────────────────────────────────

def delete_contact(db: Session, contact_id: UUID):
    contact = get_contact(db, contact_id)
    if not contact:
        return False
    db.delete(contact)
    db.commit()
    return True


# ── REFERENSI ──────────────────────────────────────────────────────────────────

def get_ref_agama(db: Session):
    return db.query(models.RefAgama).all()

def get_ref_status_perkawinan(db: Session):
    return db.query(models.RefStatusPerkawinan).all()

def get_ref_jenis_kelamin(db: Session):
    return db.query(models.RefJenisKelamin).all()
