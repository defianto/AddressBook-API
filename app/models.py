from sqlalchemy import Column, String, Boolean, Date, SmallInteger, Text, DateTime, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base


class RefAgama(Base):
    __tablename__ = "ref_agama"

    id = Column(SmallInteger, primary_key=True)
    nama_agama = Column(String(20), nullable=False)


class RefStatusPerkawinan(Base):
    __tablename__ = "ref_status_perkawinan"

    id = Column(SmallInteger, primary_key=True)
    status = Column(String(20), nullable=False)


class RefJenisKelamin(Base):
    __tablename__ = "ref_jenis_kelamin"

    id = Column(String(1), primary_key=True)
    jenis_kelamin = Column(String(10), nullable=False)


class AddressBook(Base):
    __tablename__ = "address_book"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Identitas Diri
    nama = Column(String(50), nullable=False)
    nama_lengkap = Column(String(100), nullable=False)
    nama_alias = Column(String(50))
    jenis_kelamin = Column(String(1))
    tempat_lahir = Column(String(50))
    tanggal_lahir = Column(Date)
    agama_id = Column(SmallInteger)
    status_perkawinan_id = Column(SmallInteger)
    pekerjaan = Column(String(100))
    perusahaan = Column(String(100))
    jabatan = Column(String(100))
    nik = Column(String(16))

    # Alamat Rumah
    alamat = Column(String(200))
    rt = Column(String(3))
    rw = Column(String(3))
    kelurahan = Column(String(50))
    kecamatan = Column(String(50))
    kota = Column(String(50))
    provinsi = Column(String(50))
    kode_pos = Column(String(5))
    negara = Column(String(50), default="Indonesia")

    # Alamat Domisili
    alamat_domisili = Column(String(200))
    rt_domisili = Column(String(3))
    rw_domisili = Column(String(3))
    kelurahan_domisili = Column(String(50))
    kecamatan_domisili = Column(String(50))
    kota_domisili = Column(String(50))
    provinsi_domisili = Column(String(50))
    kode_pos_domisili = Column(String(5))
    negara_domisili = Column(String(50))

    # Kontak
    email = Column(String(100))
    email_alternatif = Column(String(100))
    no_hp = Column(String(15))
    no_hp_alternatif = Column(String(15))
    no_telepon = Column(String(15))
    no_telepon_kantor = Column(String(15))
    no_fax = Column(String(15))
    no_wa = Column(String(15))

    # Media Sosial
    instagram = Column(String(50))
    facebook = Column(String(100))
    twitter = Column(String(50))
    linkedin = Column(String(100))

    # Informasi Tambahan
    foto = Column(String(255))
    catatan = Column(Text)
    grup = Column(String(50))
    is_favorite = Column(Boolean, default=False)

    # Audit
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class AppUser(Base):
    __tablename__ = "app_user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    nama_lengkap = Column(String(100), nullable=False)
    email = Column(String(100))
    role = Column(String(20), nullable=False, default="USER")
    aktif = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
