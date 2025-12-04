from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Query
from fastapi.responses import JSONResponse, FileResponse, Response, HTMLResponse
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

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """資料匯出/下載儀表板 - HTML 頁面"""
    
    # 取得統計資訊
    vlogs_count = await app.mongodb["vlogs"].count_documents({})
    sentiments_count = await app.mongodb["sentiments"].count_documents({})
    gps_count = await app.mongodb["gps_coordinates"].count_documents({})
    
    # 取得最新的幾筆資料預覽
    recent_vlogs = await app.mongodb["vlogs"].find().sort("_id", -1).limit(5).to_list(5)
    recent_sentiments = await app.mongodb["sentiments"].find().sort("_id", -1).limit(5).to_list(5)
    recent_gps = await app.mongodb["gps_coordinates"].find().sort("_id", -1).limit(5).to_list(5)
    
    # 轉換 ObjectId 為字串
    for item in recent_vlogs + recent_sentiments + recent_gps:
        item["_id"] = str(item["_id"])
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EmoGo Backend - 資料匯出儀表板</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft JhengHei', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            .header {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-bottom: 30px;
                text-align: center;
            }}
            h1 {{
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            .subtitle {{
                color: #666;
                font-size: 1.1em;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .stat-card {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                text-align: center;
                transition: transform 0.3s;
            }}
            .stat-card:hover {{
                transform: translateY(-5px);
            }}
            .stat-number {{
                font-size: 3em;
                font-weight: bold;
                color: #667eea;
                margin: 10px 0;
            }}
            .stat-label {{
                color: #666;
                font-size: 1.1em;
            }}
            .export-section {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-bottom: 20px;
            }}
            h2 {{
                color: #667eea;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #667eea;
            }}
            .export-buttons {{
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                margin-bottom: 20px;
            }}
            .btn {{
                padding: 12px 30px;
                border: none;
                border-radius: 8px;
                font-size: 1em;
                cursor: pointer;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                transition: all 0.3s;
                font-weight: 600;
            }}
            .btn-primary {{
                background: #667eea;
                color: white;
            }}
            .btn-primary:hover {{
                background: #5568d3;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }}
            .btn-success {{
                background: #48bb78;
                color: white;
            }}
            .btn-success:hover {{
                background: #38a169;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(72, 187, 120, 0.4);
            }}
            .preview-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
                overflow-x: auto;
                display: block;
            }}
            .preview-table th {{
                background: #667eea;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }}
            .preview-table td {{
                padding: 12px;
                border-bottom: 1px solid #e2e8f0;
            }}
            .preview-table tr:hover {{
                background: #f7fafc;
            }}
            .icon {{
                font-size: 1.5em;
            }}
            .footer {{
                text-align: center;
                color: white;
                margin-top: 30px;
                padding: 20px;
            }}
            .api-link {{
                color: white;
                text-decoration: none;
                font-weight: 600;
                padding: 10px 20px;
                background: rgba(255,255,255,0.2);
                border-radius: 8px;
                display: inline-block;
                margin-top: 10px;
                transition: all 0.3s;
            }}
            .api-link:hover {{
                background: rgba(255,255,255,0.3);
            }}
            .empty-state {{
                text-align: center;
                padding: 40px;
                color: #999;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎭 EmoGo Backend</h1>
                <p class="subtitle">情緒日誌資料匯出儀表板 | Data Export Dashboard</p>
            </div>

            <div class="stats">
                <div class="stat-card">
                    <div class="icon">📹</div>
                    <div class="stat-number">{vlogs_count}</div>
                    <div class="stat-label">Vlogs 影片日誌</div>
                </div>
                <div class="stat-card">
                    <div class="icon">💭</div>
                    <div class="stat-number">{sentiments_count}</div>
                    <div class="stat-label">Sentiments 情緒資料</div>
                </div>
                <div class="stat-card">
                    <div class="icon">📍</div>
                    <div class="stat-number">{gps_count}</div>
                    <div class="stat-label">GPS 座標資料</div>
                </div>
            </div>

            <div class="export-section">
                <h2>📹 Vlogs 影片日誌</h2>
                <div class="export-buttons">
                    <a href="/export/vlogs" class="btn btn-primary" target="_blank">
                        👁️ 查看資料 (JSON)
                    </a>
                    <a href="/export/vlogs?download=true" class="btn btn-success">
                        ⬇️ 下載資料檔案
                    </a>
                </div>
                {_render_preview_table(recent_vlogs, ["title", "description", "timestamp"], "無影片日誌資料")}
            </div>

            <div class="export-section">
                <h2>💭 Sentiments 情緒資料</h2>
                <div class="export-buttons">
                    <a href="/export/sentiments" class="btn btn-primary" target="_blank">
                        👁️ 查看資料 (JSON)
                    </a>
                    <a href="/export/sentiments?download=true" class="btn btn-success">
                        ⬇️ 下載資料檔案
                    </a>
                </div>
                {_render_preview_table(recent_sentiments, ["emotion", "intensity", "note", "timestamp"], "無情緒資料")}
            </div>

            <div class="export-section">
                <h2>📍 GPS Coordinates GPS 座標</h2>
                <div class="export-buttons">
                    <a href="/export/gps" class="btn btn-primary" target="_blank">
                        👁️ 查看資料 (JSON)
                    </a>
                    <a href="/export/gps?download=true" class="btn btn-success">
                        ⬇️ 下載資料檔案
                    </a>
                </div>
                {_render_preview_table(recent_gps, ["latitude", "longitude", "accuracy", "timestamp"], "無 GPS 資料")}
            </div>

            <div class="footer">
                <p>📚 <a href="/docs" class="api-link">查看完整 API 文件 (Swagger UI)</a></p>
                <p style="margin-top: 10px; opacity: 0.8;">
                    Psychoinformatics & Neuroinformatics<br>
                    By Tsung-Ren (Tren) Huang
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def _render_preview_table(data: list, fields: list, empty_message: str) -> str:
    """輔助函數：渲染資料預覽表格"""
    if not data:
        return f'<div class="empty-state">{empty_message}</div>'
    
    headers = "".join(f"<th>{field}</th>" for field in fields)
    rows = ""
    for item in data[:5]:  # 只顯示前 5 筆
        row_data = "".join(f"<td>{str(item.get(field, 'N/A'))[:50]}</td>" for field in fields)
        rows += f"<tr>{row_data}</tr>"
    
    return f"""
    <table class="preview-table">
        <thead><tr>{headers}</tr></thead>
        <tbody>{rows}</tbody>
    </table>
    <p style="margin-top: 10px; color: #999; font-size: 0.9em;">顯示最新 {len(data)} 筆資料（預覽）</p>
    """

@app.get("/api")
async def api_info():
    """API 資訊（JSON 格式）"""
    return {
        "message": "歡迎使用 EmoGo Backend API",
        "version": "1.0.0",
        "endpoints": {
            "dashboard": "/ (HTML Dashboard)",
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
async def export_sentiments(download: bool = Query(False, description="設為 true 可下載檔案")):
    """匯出所有情緒資料（資料下載頁面）"""
    sentiments = await app.mongodb["sentiments"].find().to_list(None)
    for sentiment in sentiments:
        sentiment["_id"] = str(sentiment["_id"])
    
    content = {
        "type": "sentiments",
        "total_count": len(sentiments),
        "exported_at": datetime.now().isoformat(),
        "data": sentiments
    }
    
    # 如果 download=true，觸發檔案下載
    if download:
        filename = f"sentiments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        return Response(
            content=json.dumps(content, ensure_ascii=False, indent=2),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    return JSONResponse(content=content)

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
async def export_gps_coordinates(download: bool = Query(False, description="設為 true 可下載檔案")):
    """匯出所有 GPS 座標資料（資料下載頁面）"""
    coordinates = await app.mongodb["gps_coordinates"].find().to_list(None)
    for coord in coordinates:
        coord["_id"] = str(coord["_id"])
    
    content = {
        "type": "gps_coordinates",
        "total_count": len(coordinates),
        "exported_at": datetime.now().isoformat(),
        "data": coordinates
    }
    
    # 如果 download=true，觸發檔案下載
    if download:
        filename = f"gps_coordinates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        return Response(
            content=json.dumps(content, ensure_ascii=False, indent=2),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    return JSONResponse(content=content)

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
async def export_vlogs(download: bool = Query(False, description="設為 true 可下載檔案")):
    """匯出所有影片日誌資料（資料下載頁面）"""
    vlogs = await app.mongodb["vlogs"].find().to_list(None)
    for vlog in vlogs:
        vlog["_id"] = str(vlog["_id"])
    
    content = {
        "type": "vlogs",
        "total_count": len(vlogs),
        "exported_at": datetime.now().isoformat(),
        "data": vlogs
    }
    
    # 如果 download=true，觸發檔案下載
    if download:
        filename = f"vlogs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        return Response(
            content=json.dumps(content, ensure_ascii=False, indent=2),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    return JSONResponse(content=content)

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
