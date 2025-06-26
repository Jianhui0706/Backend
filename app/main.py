from fastapi import FastAPI
from app.auth.router import router as auth_router

app = FastAPI()

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# for the auth router
app.include_router(auth_router)