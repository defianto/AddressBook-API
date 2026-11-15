import os
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pepper: string rahasia dari environment variable, tidak disimpan di database.
# Jika database bocor, hash tetap tidak bisa di-crack tanpa nilai pepper ini.
PEPPER = os.getenv("PASSWORD_PEPPER", "")


def _add_pepper(plain: str) -> str:
    """Tambahkan pepper ke password sebelum di-hash."""
    return plain + PEPPER


def hash_password(plain: str) -> str:
    """Enkripsi password menggunakan BCrypt + Pepper."""
    return pwd_context.hash(_add_pepper(plain))


def verify_password(plain: str, hashed: str) -> bool:
    """Verifikasi password plain + pepper terhadap hash BCrypt."""
    return pwd_context.verify(_add_pepper(plain), hashed)
