from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import contacts, references, users, auth

# Buat semua tabel (jika belum ada)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Address Book API",
    description="API untuk manajemen kontak Address Book dengan PostgreSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — izinkan semua origin (sesuaikan di production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(references.router)
app.include_router(users.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "app": "Address Book API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Root"])
def health():
    return {"status": "ok"}
