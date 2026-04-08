from typing import List, Optional
from bson import ObjectId

from app.models.scan import ScanCreate, ScanInDB
from app.dependencies import get_database
class ScanService:
    def __init__(self,db):
        self.db = db
        self.collection = db["scans"]
    
    async def create_scan(self, scan_data: ScanCreate) -> ScanInDB:
        scan_dict = scan_data.model_dump()
        result = await self.collection.insert_one(scan_dict)
        scan_dict["_id"] = str(result.inserted_id)
        return ScanInDB(**scan_dict)

    async def get_scan(self, scan_id: str) -> Optional[ScanInDB]:
        if not ObjectId.is_valid(scan_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(scan_id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            return ScanInDB(**doc)
        return None
    
    async def list_scans(self, limit: int = 10) -> List[ScanInDB]:
        cursor = self.collection.find().limit(limit)
        scans = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            scans.append(ScanInDB(**doc))
        return scans

    async def delete_scan(self, scan_id: str) -> bool:
        if not ObjectId.is_valid(scan_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(scan_id)})
        return result.deleted_count > 0