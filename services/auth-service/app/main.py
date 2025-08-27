import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from jose import jwt, JWTError

from app import app
from .models import Base, User
from .schemas import UserCreate, Token
from .auth import hash_password, verify_password, create_access_token


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")
JWT_SECRET = os.getenv("JWT_SECRET", "devsecretchange")
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "240"))


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Auth Service")


@app.post("/auth/signup", response_model=Token)
def signup(payload: UserCreate):
 db = SessionLocal()
 try:
   user = User(username=payload.username, password_hash=hash_password(payload.password))
   db.add(user)
   db.commit()
   db.refresh(user)
   token = create_access_token({"sub": user.username, "uid": user.id}, JWT_SECRET, ACCESS_TOKEN_MINUTES)
   return {"access_token": token, "token_type": "bearer"}
 except IntegrityError:
  db.rollback()
  raise HTTPException(status_code=400, detail="Username already exists")
 finally:
  db.close()


@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
  db = SessionLocal()
  try:
   user = db.query(User).filter(User.username == form_data.username).first()
   if not user or not verify_password(form_data.password, user.password_hash):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.username, "uid": user.id}, JWT_SECRET, ACCESS_TOKEN_MINUTES)
   return {"access_token": token, "token_type": "bearer"}
  finally:
    db.close()


@app.get("/auth/health")
def health():
 return {"status": "ok"}