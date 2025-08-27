import os
from fastapi import FastAPI, Header, HTTPException
import httpx
from jose import jwt, JWTError


AUTH_PUBLIC = os.getenv("AUTH_JWT_SECRET", "devsecretchange")
CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog-service:8001")


app = FastAPI(title="Gateway Service")


@app.get("/api/health")
def health():
 return {"status": "ok"}


@app.get("/api/songs")
async def songs(authorization: str | None = Header(default=None)):
 if not authorization or not authorization.startswith("Bearer "):
  raise HTTPException(status_code=401, detail="Missing bearer token")
  token = authorization.split(" ", 1)[1]
 try:
  jwt.get_unverified_header(token) # basic header check
  jwt.decode(token, AUTH_PUBLIC, algorithms=["HS256"]) # shared secret for demo
 except JWTError:
  raise HTTPException(status_code=401, detail="Invalid token")


 async with httpx.AsyncClient() as client:
  r = await client.get(f"{CATALOG_URL}/songs", timeout=10)
  r.raise_for_status()
 return r.json()