from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.dependencies import get_database
from app.models.scan import ScanCreate, ScanInDB
from app.services.scan_service import ScanService

router = APIRouter(prefix="/scans", tags=["scans"])

async def get_scan_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> ScanService:
    return ScanService(db)

@router.post("/", response_model=ScanInDB, status_code=status.HTTP_201_CREATED)
async def create_scan(scan: ScanCreate, service: ScanService = Depends(get_scan_service)):
    return await service.create_scan(scan)

@router.get("/{scan_id}", response_model=ScanInDB)
async def get_scan(scan_id: str, service: ScanService = Depends(get_scan_service)):
    scan = await service.get_scan(scan_id)
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")
    return scan

@router.get("/", response_model=list[ScanInDB])
async def list_scans(limit: int = 10, service: ScanService = Depends(get_scan_service)):
    return await service.list_scans(limit)

@router.delete("/{scan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scan(scan_id: str, service: ScanService = Depends(get_scan_service)):
    deleted = await service.delete_scan(scan_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")
