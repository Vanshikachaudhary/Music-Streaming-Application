from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def hash_password(password: str) -> str:
  return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
  return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, secret_key: str, expires_minutes: int = 60) -> str:
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)