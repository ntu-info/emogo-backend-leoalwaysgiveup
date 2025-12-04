# EmoGo Backend API

> 情緒日誌後端系統 - 使用 FastAPI + MongoDB  
> Psychoinformatics & Neuroinformatics 課程作業  
> By Tsung-Ren (Tren) Huang

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/e7FBMwSa)

---

## 📊 資料匯出/下載頁面 URI（作業要求）

部署後，請將 `https://your-app-name.onrender.com` 替換為你的實際網址：

### 🎯 三種資料類型的匯出端點：

1. **📹 Vlogs（影片日誌）**  
   ```
   GET https://your-app-name.onrender.com/export/vlogs
   ```

2. **💭 Sentiments（情緒資料）**  
   ```
   GET https://your-app-name.onrender.com/export/sentiments
   ```

3. **📍 GPS Coordinates（GPS 座標）**  
   ```
   GET https://your-app-name.onrender.com/export/gps
   ```

### 📈 統計資訊端點：
```
GET https://your-app-name.onrender.com/stats
```

### 📚 完整 API 文件：
```
GET https://your-app-name.onrender.com/docs
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

---

## 📡 API Endpoints

### 基本路由

| Method | Endpoint | 說明 |
|--------|----------|------|
| GET | `/` | API 首頁資訊 |
| GET | `/health` | 健康檢查 |
| GET | `/stats` | 統計資訊 |
| GET | `/docs` | Swagger API 文件 |

### Sentiments（情緒資料）

| Method | Endpoint | 說明 |
|--------|----------|------|
| POST | `/sentiments` | 新增情緒資料 |
| GET | `/sentiments` | 取得情緒資料列表 |
| GET | `/export/sentiments` | **匯出所有情緒資料** ⭐ |

**範例請求 (POST /sentiments):**
```json
{
  "user_id": "user123",
  "emotion": "happy",
  "intensity": 0.85,
  "note": "今天天氣很好！",
  "timestamp": "2024-12-04T10:30:00Z"
}
```

### GPS Coordinates（GPS 座標）

| Method | Endpoint | 說明 |
|--------|----------|------|
| POST | `/gps` | 新增 GPS 座標 |
| GET | `/gps` | 取得 GPS 座標列表 |
| GET | `/export/gps` | **匯出所有 GPS 座標** ⭐ |

**範例請求 (POST /gps):**
```json
{
  "user_id": "user123",
  "latitude": 25.0330,
  "longitude": 121.5654,
  "accuracy": 10.5,
  "timestamp": "2024-12-04T10:30:00Z"
}
```

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

## 🔧 部署到 Render

### 步驟 1：設定 MongoDB Atlas

1. 前往 [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) 註冊並建立免費叢集
2. 在 Security > Network Access 中，將 IP 白名單設定為 `0.0.0.0/0`（允許所有 IP）
3. 在 Security > Database Access 中，建立資料庫使用者
4. 取得連接字串（Connection String），格式如：
   ```
   mongodb+srv://username:password@cluster.mongodb.net/
   ```

### 步驟 2：部署到 Render

1. 將程式碼推送到 GitHub
2. 前往 [Render](https://render.com/) 並登入
3. 點選 **New +** → **Web Service**
4. 連接你的 GitHub repository
5. 設定如下：
   - **Name**: 選擇一個名稱（例如：emogo-backend）
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

6. 在 **Environment Variables** 中新增：
   - `MONGODB_URI`: 你的 MongoDB 連接字串
   - `DB_NAME`: `emogo_db`（或你想要的資料庫名稱）

7. 點選 **Create Web Service**

8. 等待部署完成後，你會得到一個 URL，例如：
   ```
   https://emogo-backend-xxxx.onrender.com
   ```

9. **記得回到這個 README.md 更新上方的 URL！**

---

## 🧪 測試 API

### 使用 curl 測試

**新增情緒資料：**
```bash
curl -X POST "https://your-app-name.onrender.com/sentiments" \
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
curl "https://your-app-name.onrender.com/export/sentiments"
```

### 使用瀏覽器測試

直接在瀏覽器中開啟以下網址：
- https://your-app-name.onrender.com/docs （互動式 API 文件）
- https://your-app-name.onrender.com/export/vlogs
- https://your-app-name.onrender.com/export/sentiments
- https://your-app-name.onrender.com/export/gps

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

## 📝 作業要求檢查清單

- [x] 使用 FastAPI 建立後端
- [x] 使用 MongoDB 儲存資料
- [x] 支援三種資料類型：vlogs, sentiments, GPS coordinates
- [x] 提供資料匯出/下載 API endpoints
- [x] 在 README.md 中列出資料匯出 URI
- [x] 部署到公開伺服器（Render）
- [x] 助教和老師可以透過 URI 查看/下載所有資料

---

## 📧 聯絡資訊

如有問題，請聯絡助教或在課程討論區發問。

---

## 📄 授權

此專案為課程作業，僅供學習使用。

---

**🎓 Psychoinformatics & Neuroinformatics - Week 11**  
**👨‍🏫 Instructor: Tsung-Ren (Tren) Huang**
