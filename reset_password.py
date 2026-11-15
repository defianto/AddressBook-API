import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()

PEPPER = os.getenv("PASSWORD_PEPPER", "")


def hash_password(plain: str) -> str:
    combined = (plain + PEPPER).encode("utf-8")
    return bcrypt.hashpw(combined, bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    combined = (plain + PEPPER).encode("utf-8")
    return bcrypt.checkpw(combined, hashed.encode("utf-8"))


def main():
    print("=" * 45)
    print("       RESET PASSWORD ADDRESBOOK")
    print("=" * 45)

    if not PEPPER:
        print("⚠ WARNING: PASSWORD_PEPPER tidak ditemukan di environment variable!")
        print("  Pastikan sudah di-set sebelum menjalankan script ini.\n")

    username     = input("Username       : ")
    password_baru = input("Password baru  : ")
    konfirmasi   = input("Konfirmasi     : ")

    if password_baru != konfirmasi:
        print("\n✘ Password dan konfirmasi tidak cocok.")
        return

    hash_baru = hash_password(password_baru)

    print("\n" + "─" * 45)
    print("✔ Hash berhasil dibuat!")
    print("─" * 45)
    print(f"Username : {username}")
    print(f"Hash     : {hash_baru}")
    print("─" * 45)
    print("\nJalankan query berikut di database:")
    print(f"\n  UPDATE app_user")
    print(f"  SET password = '{hash_baru}'")
    print(f"  WHERE username = '{username}';")
    print()


if __name__ == "__main__":
    main()
