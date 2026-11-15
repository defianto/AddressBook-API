-- Address Book database schema (PostgreSQL)
-- Sumber: address-book-V2.sql + Create_app_user.sql (tanpa user admin default)
-- Buat user admin dengan reset_password.py, lihat README.

-- Buat Database
CREATE DATABASE address_book;

-- Koneksikan ke database
\c address_book;

-- Buat extension untuk UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabel Referensi Agama
CREATE TABLE ref_agama (
    id          SMALLINT PRIMARY KEY,
    nama_agama  VARCHAR(20) NOT NULL
);

INSERT INTO ref_agama VALUES
(1, 'Islam'),
(2, 'Kristen Protestan'),
(3, 'Kristen Katolik'),
(4, 'Hindu'),
(5, 'Buddha'),
(6, 'Konghucu'),
(7, 'Lainnya');

-- Tabel Referensi Status Perkawinan
CREATE TABLE ref_status_perkawinan (
    id      SMALLINT PRIMARY KEY,
    status  VARCHAR(20) NOT NULL
);

INSERT INTO ref_status_perkawinan VALUES
(1, 'Belum Menikah'),
(2, 'Menikah'),
(3, 'Cerai Hidup'),
(4, 'Cerai Mati'),
(5, 'Janda'),
(6, 'Duda');

-- Tabel Referensi Jenis Kelamin
CREATE TABLE ref_jenis_kelamin (
    id             VARCHAR(1) PRIMARY KEY,
    jenis_kelamin   VARCHAR(10) NOT NULL
);

INSERT INTO ref_jenis_kelamin VALUES
('L', 'Laki-laki'),
('P', 'Perempuan');

-- Tabel Utama Address Book
CREATE TABLE address_book (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Identitas Diri
    nama                VARCHAR(50)  NOT NULL,       -- nama panggilan
    nama_lengkap        VARCHAR(100) NOT NULL,       -- nama lengkap sesuai KTP
    nama_alias          VARCHAR(50),                 -- nama lain / alias
    jenis_kelamin      VARCHAR(1) REFERENCES ref_jenis_kelamin(id),
    tempat_lahir        VARCHAR(50),                 -- kota tempat lahir
    tanggal_lahir       DATE,
    agama_id            SMALLINT REFERENCES ref_agama(id),
    status_perkawinan_id SMALLINT REFERENCES ref_status_perkawinan(id),
    pekerjaan           VARCHAR(100),
    perusahaan          VARCHAR(100),                -- nama perusahaan/instansi
    jabatan             VARCHAR(100),                -- jabatan/posisi
    nik                VARCHAR(16),                    -- nomor KTP

    -- Alamat Rumah
    alamat              VARCHAR(200),                -- nama jalan + nomor rumah
    rt                 VARCHAR(3),                     -- RT (contoh: 001)
    rw                 VARCHAR(3),                     -- RW (contoh: 005)
    kelurahan           VARCHAR(50),
    kecamatan           VARCHAR(50),
    kota                VARCHAR(50),
    provinsi            VARCHAR(50),
    kode_pos           VARCHAR(5),
    negara              VARCHAR(50) DEFAULT 'Indonesia',

    -- Alamat Domisili (jika berbeda)
    alamat_domisili     VARCHAR(200),
    rt_domisili        VARCHAR(3),
    rw_domisili        VARCHAR(3),
    kelurahan_domisili  VARCHAR(50),
    kecamatan_domisili  VARCHAR(50),
    kota_domisili       VARCHAR(50),
    provinsi_domisili   VARCHAR(50),
    kode_pos_domisili  VARCHAR(5),
    negara_domisili     VARCHAR(50),

    -- Kontak
    email               VARCHAR(100),
    email_alternatif    VARCHAR(100),
    no_hp               VARCHAR(15),                 -- nomor handphone
    no_hp_alternatif    VARCHAR(15),
    no_telepon          VARCHAR(15),                 -- nomor telepon rumah
    no_telepon_kantor   VARCHAR(15),
    no_fax              VARCHAR(15),
    no_wa               VARCHAR(15),                 -- nomor whatsapp

    -- Media Sosial
    instagram           VARCHAR(50),
    facebook            VARCHAR(100),
    twitter             VARCHAR(50),
    linkedin            VARCHAR(100),

    -- Informasi Tambahan
    foto                VARCHAR(255),                -- path/URL foto
    catatan             TEXT,                        -- catatan bebas
    grup                VARCHAR(50),                 -- kategori: Keluarga, Teman, Kerja, dll
    is_favorite         BOOLEAN DEFAULT FALSE,

    -- Audit
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index untuk pencarian
CREATE INDEX idx_nama ON address_book(nama);
CREATE INDEX idx_nama_lengkap ON address_book(nama_lengkap);
CREATE INDEX idx_email ON address_book(email);
CREATE INDEX idx_no_hp ON address_book(no_hp);
CREATE INDEX idx_kota ON address_book(kota);
CREATE INDEX idx_grup ON address_book(grup);

-- Trigger untuk update otomatis kolom updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_updated_at
BEFORE UPDATE ON address_book
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- Contoh Insert Data
INSERT INTO address_book (
    nama, nama_lengkap, jenis_kelamin,
    tempat_lahir, tanggal_lahir,
    agama_id, status_perkawinan_id, pekerjaan,
    alamat, rt, rw, kelurahan, kecamatan,
    kota, provinsi, kode_pos, negara,
    email, no_hp, grup
) VALUES (
    'Budi',
    'Budi Santoso',
    'L',
    'Bandung',
    '1990-05-15',
    1,
    2,
    'Pegawai Swasta',
    'Jl. Merdeka No. 10',
    '003', '005',
    'Sukajadi',
    'Sukajadi',
    'Bandung',
    'Jawa Barat',
    '40162',
    'Indonesia',
    'budi.santoso@email.com',
    '08123456789',
    'Teman'
);

CREATE TABLE app_user (
    id           BIGSERIAL PRIMARY KEY,
    username     VARCHAR(50)  NOT NULL UNIQUE,
    password     VARCHAR(255) NOT NULL,
    nama_lengkap VARCHAR(100) NOT NULL,
    email        VARCHAR(100),
    role         VARCHAR(20)  NOT NULL DEFAULT 'USER',
    aktif        BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- Trigger updated_at
CREATE TRIGGER trg_app_user_updated_at
BEFORE UPDATE ON app_user
FOR EACH ROW EXECUTE FUNCTION update_updated_at();

