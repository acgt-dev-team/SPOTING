from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.session import engine, Base
from app.api import wizard

app = FastAPI(
    title="SPOTING Backend",
    version="1.0"
)

# Allow frontend to access backend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(wizard.router)

@app.get("/")
def root():
    return {"message": "SPOTING backend running"}

@app.get("/health")
def health():
    return {"status": "ok"}