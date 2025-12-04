from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
import json

# MongoDB 設定 - 從環境變數讀取
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "emogo_db")

app = FastAPI(
    title="EmoGo Backend API",
    description="情緒日誌後端系統 - 支援 vlogs, sentiments, GPS coordinates",
    version="1.0.0"
)

# ===== 資料模型定義 =====

class Sentiment(BaseModel):
    """情緒資料模型"""
    user_id: Optional[str] = None
    emotion: str  # 例如: happy, sad, angry, neutral
    intensity: float  # 0.0 - 1.0
    note: Optional[str] = None
    timestamp: Optional[str] = None

class GPSCoordinate(BaseModel):
    """GPS 座標資料模型"""
    user_id: Optional[str] = None
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    timestamp: Optional[str] = None

class Vlog(BaseModel):
    """影片日誌資料模型"""
    user_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    video_url: Optional[str] = None
    duration: Optional[float] = None
    timestamp: Optional[str] = None

# ===== MongoDB 連接管理 =====

@app.on_event("startup")
async def startup_db_client():
    """啟動時連接 MongoDB"""
    app.mongodb_client = AsyncIOMotorClient(MONGODB_URI)
    app.mongodb = app.mongodb_client[DB_NAME]
    print(f"✅ Connected to MongoDB: {DB_NAME}")

@app.on_event("shutdown")
async def shutdown_db_client():
    """關閉時斷開 MongoDB 連接"""
    app.mongodb_client.close()
    print("❌ Disconnected from MongoDB")

# ===== 基本路由 =====

@app.get("/")
async def root():
    """首頁 - API 資訊"""
    return {
        "message": "歡迎使用 EmoGo Backend API",
        "version": "1.0.0",
        "endpoints": {
            "vlogs": "/vlogs (POST), /export/vlogs (GET)",
            "sentiments": "/sentiments (POST), /export/sentiments (GET)",
            "gps": "/gps (POST), /export/gps (GET)"
        },
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """健康檢查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ===== Sentiments API =====

@app.post("/sentiments")
async def create_sentiment(sentiment: Sentiment):
    """新增情緒資料"""
    sentiment_dict = sentiment.dict()
    if not sentiment_dict.get("timestamp"):
        sentiment_dict["timestamp"] = datetime.now().isoformat()
    
    result = await app.mongodb["sentiments"].insert_one(sentiment_dict)
    sentiment_dict["_id"] = str(result.inserted_id)
    
    return {
        "status": "success",
        "message": "情緒資料已儲存",
        "data": sentiment_dict
    }

@app.get("/sentiments")
async def get_sentiments(limit: int = 100):
    """取得情緒資料列表"""
    sentiments = await app.mongodb["sentiments"].find().limit(limit).to_list(limit)
    for sentiment in sentiments:
        sentiment["_id"] = str(sentiment["_id"])
    return {"count": len(sentiments), "data": sentiments}

@app.get("/export/sentiments")
async def export_sentiments():
    """匯出所有情緒資料（資料下載頁面）"""
    sentiments = await app.mongodb["sentiments"].find().to_list(None)
    for sentiment in sentiments:
        sentiment["_id"] = str(sentiment["_id"])
    
    return JSONResponse(
        content={
            "type": "sentiments",
            "total_count": len(sentiments),
            "exported_at": datetime.now().isoformat(),
            "data": sentiments
        }
    )

# ===== GPS Coordinates API =====

@app.post("/gps")
async def create_gps_coordinate(gps: GPSCoordinate):
    """新增 GPS 座標資料"""
    gps_dict = gps.dict()
    if not gps_dict.get("timestamp"):
        gps_dict["timestamp"] = datetime.now().isoformat()
    
    result = await app.mongodb["gps_coordinates"].insert_one(gps_dict)
    gps_dict["_id"] = str(result.inserted_id)
    
    return {
        "status": "success",
        "message": "GPS 座標已儲存",
        "data": gps_dict
    }

@app.get("/gps")
async def get_gps_coordinates(limit: int = 100):
    """取得 GPS 座標列表"""
    coordinates = await app.mongodb["gps_coordinates"].find().limit(limit).to_list(limit)
    for coord in coordinates:
        coord["_id"] = str(coord["_id"])
    return {"count": len(coordinates), "data": coordinates}

@app.get("/export/gps")
async def export_gps_coordinates():
    """匯出所有 GPS 座標資料（資料下載頁面）"""
    coordinates = await app.mongodb["gps_coordinates"].find().to_list(None)
    for coord in coordinates:
        coord["_id"] = str(coord["_id"])
    
    return JSONResponse(
        content={
            "type": "gps_coordinates",
            "total_count": len(coordinates),
            "exported_at": datetime.now().isoformat(),
            "data": coordinates
        }
    )

# ===== Vlogs API =====

@app.post("/vlogs")
async def create_vlog(vlog: Vlog):
    """新增影片日誌資料"""
    vlog_dict = vlog.dict()
    if not vlog_dict.get("timestamp"):
        vlog_dict["timestamp"] = datetime.now().isoformat()
    
    result = await app.mongodb["vlogs"].insert_one(vlog_dict)
    vlog_dict["_id"] = str(result.inserted_id)
    
    return {
        "status": "success",
        "message": "影片日誌已儲存",
        "data": vlog_dict
    }

@app.get("/vlogs")
async def get_vlogs(limit: int = 100):
    """取得影片日誌列表"""
    vlogs = await app.mongodb["vlogs"].find().limit(limit).to_list(limit)
    for vlog in vlogs:
        vlog["_id"] = str(vlog["_id"])
    return {"count": len(vlogs), "data": vlogs}

@app.get("/export/vlogs")
async def export_vlogs():
    """匯出所有影片日誌資料（資料下載頁面）"""
    vlogs = await app.mongodb["vlogs"].find().to_list(None)
    for vlog in vlogs:
        vlog["_id"] = str(vlog["_id"])
    
    return JSONResponse(
        content={
            "type": "vlogs",
            "total_count": len(vlogs),
            "exported_at": datetime.now().isoformat(),
            "data": vlogs
        }
    )

# ===== 統計資訊 API =====

@app.get("/stats")
async def get_statistics():
    """取得所有資料的統計資訊"""
    vlogs_count = await app.mongodb["vlogs"].count_documents({})
    sentiments_count = await app.mongodb["sentiments"].count_documents({})
    gps_count = await app.mongodb["gps_coordinates"].count_documents({})
    
    return {
        "total_records": vlogs_count + sentiments_count + gps_count,
        "vlogs": vlogs_count,
        "sentiments": sentiments_count,
        "gps_coordinates": gps_count,
        "timestamp": datetime.now().isoformat()
    }

# ===== 批次刪除 API（測試用途）=====

@app.delete("/clear/{collection_name}")
async def clear_collection(collection_name: str):
    """清空指定的 collection（僅供測試使用）"""
    if collection_name not in ["vlogs", "sentiments", "gps_coordinates"]:
        raise HTTPException(status_code=400, message="Invalid collection name")
    
    result = await app.mongodb[collection_name].delete_many({})
    return {
        "status": "success",
        "message": f"已清空 {collection_name}",
        "deleted_count": result.deleted_count
    }
