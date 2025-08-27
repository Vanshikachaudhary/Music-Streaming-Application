from fastapi import FastAPI, Request
import httpx

app = FastAPI(title="Spotify Clone - API Gateway")

# Internal service URLs (match the exposed ports of each microservice)
AUTH_SERVICE_URL = "http://auth-service:8000"
CATALOG_SERVICE_URL = "http://catalog-service:8001"  # ✅ fixed to 8001


# ------------------------
# Proxy: Auth Service
# ------------------------
@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_auth(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"{AUTH_SERVICE_URL}/{path}",
            headers=request.headers.raw,
            content=await request.body()
        )
    return response.json()


# ------------------------
# Proxy: Catalog Service
# ------------------------
@app.api_route("/catalog/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_catalog(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"{CATALOG_SERVICE_URL}/{path}",
            headers=request.headers.raw,
            content=await request.body()
        )
    return response.json()


# ------------------------
# Root endpoint
# ------------------------
@app.get("/")
def root():
    return {"message": "🎶 Spotify Clone API Gateway is running!"}
