from fastapi import FastAPI
from app.routers import scans

app = FastAPI(title="Alerts API", description="API for alerts management with MongoDB", version="1.0.0")

app.include_router(scans.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Alerts API"}