# EmoGo Backend API

> 情緒日誌後端系統 - 使用 FastAPI + MongoDB  
> Psychoinformatics & Neuroinformatics 課程作業  
> By Tsung-Ren (Tren) Huang

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/e7FBMwSa)

---

## 📊 資料匯出/下載頁面 URI（作業要求）

**✅ 已部署！API 網址：** `https://emogo-backend-leoalwaysgiveup.onrender.com`

### 🎯 三種資料類型的匯出端點：

1. **📹 Vlogs（影片日誌）**  
   - **查看資料**：`GET https://emogo-backend-leoalwaysgiveup.onrender.com/export/vlogs`
   - **下載檔案**：`GET https://emogo-backend-leoalwaysgiveup.onrender.com/export/vlogs?download=true` 📥

2. **💭 Sentiments（情緒資料）**  
   - **查看資料**：`GET https://emogo-backend-leoalwaysgiveup.onrender.com/export/sentiments`
   - **下載檔案**：`GET https://emogo-backend-leoalwaysgiveup.onrender.com/export/sentiments?download=true` 📥

3. **📍 GPS Coordinates（GPS 座標）**  
   - **查看資料**：`GET https://emogo-backend-leoalwaysgiveup.onrender.com/export/gps`
   - **下載檔案**：`GET https://emogo-backend-leoalwaysgiveup.onrender.com/export/gps?download=true` 📥

### 📈 統計資訊端點：
```
GET https://emogo-backend-leoalwaysgiveup.onrender.com/stats
```

### 📚 完整 API 文件：
```
GET https://emogo-backend-leoalwaysgiveup.onrender.com/docs
```

---

## 🚀 快速開始

### 本地開發

1. **安裝依賴套件**
   ```bash
   pip install -r requirements.txt
   ```

2. **設定環境變數**
   
   建立 `.env` 檔案或設定系統環境變數：
   ```bash
   export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/"
   export DB_NAME="emogo_db"
   ```

3. **啟動伺服器**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **開啟 API 文件**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc


### Vlogs（影片日誌）

| Method | Endpoint | 說明 |
|--------|----------|------|
| POST | `/vlogs` | 新增影片日誌 |
| GET | `/vlogs` | 取得影片日誌列表 |
| GET | `/export/vlogs` | **匯出所有影片日誌** ⭐ |

**範例請求 (POST /vlogs):**
```json
{
  "user_id": "user123",
  "title": "今天的心情記錄",
  "description": "分享今天發生的有趣事情",
  "video_url": "https://example.com/video.mp4",
  "duration": 120.5,
  "timestamp": "2024-12-04T10:30:00Z"
}
```

---



---

## 🧪 測試 API

### 使用 curl 測試

**新增情緒資料：**
```bash
curl -X POST "https://emogo-backend-leoalwaysgiveup.onrender.com/sentiments" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "emotion": "happy",
    "intensity": 0.9,
    "note": "測試資料"
  }'
```

**匯出資料：**
```bash
curl "https://emogo-backend-leoalwaysgiveup.onrender.com/export/sentiments"
```

### 使用瀏覽器測試

直接在瀏覽器中開啟以下網址：
- https://emogo-backend-leoalwaysgiveup.onrender.com/docs （互動式 API 文件）
- https://emogo-backend-leoalwaysgiveup.onrender.com/export/vlogs
- https://emogo-backend-leoalwaysgiveup.onrender.com/export/sentiments
- https://emogo-backend-leoalwaysgiveup.onrender.com/export/gps

---

## 📦 專案結構

```
emogo-backend/
├── main.py              # FastAPI 主程式
├── requirements.txt     # Python 依賴套件
├── render.yaml          # Render 部署設定
└── README.md           # 專案說明文件
```

---

## 🛠 技術棧

- **後端框架**: FastAPI
- **資料庫**: MongoDB (Motor - 非同步驅動)
- **部署平台**: Render
- **Python**: 3.8+

---


---

