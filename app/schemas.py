from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from uuid import UUID


# ── Referensi ──────────────────────────────────────────────────────────────────

class RefAgamaOut(BaseModel):
    id: int
    nama_agama: str
    class Config:
        from_attributes = True

class RefStatusPerkawinanOut(BaseModel):
    id: int
    status: str
    class Config:
        from_attributes = True

class RefJenisKelaminOut(BaseModel):
    id: str
    jenis_kelamin: str
    class Config:
        from_attributes = True


# ── Address Book ───────────────────────────────────────────────────────────────

class AddressBookBase(BaseModel):
    # Identitas
    nama: str
    nama_lengkap: str
    nama_alias: Optional[str] = None
    jenis_kelamin: Optional[str] = None
    tempat_lahir: Optional[str] = None
    tanggal_lahir: Optional[date] = None
    agama_id: Optional[int] = None
    status_perkawinan_id: Optional[int] = None
    pekerjaan: Optional[str] = None
    perusahaan: Optional[str] = None
    jabatan: Optional[str] = None
    nik: Optional[str] = None

    # Alamat Rumah
    alamat: Optional[str] = None
    rt: Optional[str] = None
    rw: Optional[str] = None
    kelurahan: Optional[str] = None
    kecamatan: Optional[str] = None
    kota: Optional[str] = None
    provinsi: Optional[str] = None
    kode_pos: Optional[str] = None
    negara: Optional[str] = "Indonesia"

    # Alamat Domisili
    alamat_domisili: Optional[str] = None
    rt_domisili: Optional[str] = None
    rw_domisili: Optional[str] = None
    kelurahan_domisili: Optional[str] = None
    kecamatan_domisili: Optional[str] = None
    kota_domisili: Optional[str] = None
    provinsi_domisili: Optional[str] = None
    kode_pos_domisili: Optional[str] = None
    negara_domisili: Optional[str] = None

    # Kontak
    email: Optional[str] = None
    email_alternatif: Optional[str] = None
    no_hp: Optional[str] = None
    no_hp_alternatif: Optional[str] = None
    no_telepon: Optional[str] = None
    no_telepon_kantor: Optional[str] = None
    no_fax: Optional[str] = None
    no_wa: Optional[str] = None

    # Media Sosial
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    linkedin: Optional[str] = None

    # Tambahan
    foto: Optional[str] = None
    catatan: Optional[str] = None
    grup: Optional[str] = None
    is_favorite: Optional[bool] = False


class AddressBookCreate(AddressBookBase):
    pass


class AddressBookUpdate(BaseModel):
    nama: Optional[str] = None
    nama_lengkap: Optional[str] = None
    nama_alias: Optional[str] = None
    jenis_kelamin: Optional[str] = None
    tempat_lahir: Optional[str] = None
    tanggal_lahir: Optional[date] = None
    agama_id: Optional[int] = None
    status_perkawinan_id: Optional[int] = None
    pekerjaan: Optional[str] = None
    perusahaan: Optional[str] = None
    jabatan: Optional[str] = None
    nik: Optional[str] = None
    alamat: Optional[str] = None
    rt: Optional[str] = None
    rw: Optional[str] = None
    kelurahan: Optional[str] = None
    kecamatan: Optional[str] = None
    kota: Optional[str] = None
    provinsi: Optional[str] = None
    kode_pos: Optional[str] = None
    negara: Optional[str] = None
    alamat_domisili: Optional[str] = None
    rt_domisili: Optional[str] = None
    rw_domisili: Optional[str] = None
    kelurahan_domisili: Optional[str] = None
    kecamatan_domisili: Optional[str] = None
    kota_domisili: Optional[str] = None
    provinsi_domisili: Optional[str] = None
    kode_pos_domisili: Optional[str] = None
    negara_domisili: Optional[str] = None
    email: Optional[str] = None
    email_alternatif: Optional[str] = None
    no_hp: Optional[str] = None
    no_hp_alternatif: Optional[str] = None
    no_telepon: Optional[str] = None
    no_telepon_kantor: Optional[str] = None
    no_fax: Optional[str] = None
    no_wa: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    linkedin: Optional[str] = None
    foto: Optional[str] = None
    catatan: Optional[str] = None
    grup: Optional[str] = None
    is_favorite: Optional[bool] = None


class AddressBookOut(AddressBookBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: list[AddressBookOut]


# ── App User ───────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    password: str
    nama_lengkap: str
    email: Optional[str] = None
    role: Optional[str] = "USER"
    aktif: Optional[bool] = True


class UserUpdate(BaseModel):
    nama_lengkap: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    aktif: Optional[bool] = None


class UserChangePassword(BaseModel):
    password_lama: str
    password_baru: str


class UserOut(BaseModel):
    id: int
    username: str
    nama_lengkap: str
    email: Optional[str] = None
    role: str
    aktif: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
