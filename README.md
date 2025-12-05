# EmoGo Backend API

> 情緒日誌後端系統 - FastAPI + MongoDB  
> Psychoinformatics & Neuroinformatics 課程作業

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/e7FBMwSa)

---

## 📊 資料匯出/下載頁面（作業要求）

### 🎭 主要儀表板（HTML Dashboard）⭐

**👉 請直接開啟這個網址：**

```
https://emogo-backend-leoalwaysgiveup.onrender.com/
```

**功能：**
- ✅ 互動式 HTML 頁面（由 FastAPI 產生）
- ✅ 查看三種資料的統計數量
- ✅ 預覽最新資料
- ✅ 直接點按鈕查看完整資料（JSON）
- ✅ 直接點按鈕下載資料檔案
- ✅ 訪問 API 文件

---

## 🎯 三種資料類型的直接匯出端點

如果需要直接訪問 API（不透過 Dashboard）：

### 1. 📹 Vlogs（影片日誌）
- **查看資料**：https://emogo-backend-leoalwaysgiveup.onrender.com/export/vlogs
- **下載檔案**：https://emogo-backend-leoalwaysgiveup.onrender.com/export/vlogs?download=true

### 2. 💭 Sentiments（情緒資料）
- **查看資料**：https://emogo-backend-leoalwaysgiveup.onrender.com/export/sentiments
- **下載檔案**：https://emogo-backend-leoalwaysgiveup.onrender.com/export/sentiments?download=true

### 3. 📍 GPS Coordinates（GPS 座標）
- **查看資料**：https://emogo-backend-leoalwaysgiveup.onrender.com/export/gps
- **下載檔案**：https://emogo-backend-leoalwaysgiveup.onrender.com/export/gps?download=true

---

## 📚 其他端點

- **API 文件（Swagger UI）**：https://emogo-backend-leoalwaysgiveup.onrender.com/docs
- **統計資訊**：https://emogo-backend-leoalwaysgiveup.onrender.com/stats
- **健康檢查**：https://emogo-backend-leoalwaysgiveup.onrender.com/health

---

## 🛠 技術架構

- **後端框架**：FastAPI
- **資料庫**：MongoDB Atlas（雲端）
- **部署平台**：Render
- **Python 版本**：3.13+

---

## 📡 API 功能列表

### Vlogs（影片日誌）
| 方法 | 端點 | 說明 |
|------|------|------|
| POST | `/vlogs` | 新增影片日誌 |
| GET | `/vlogs` | 取得影片列表 |
| GET | `/export/vlogs` | 匯出所有影片資料 |

### Sentiments（情緒資料）
| 方法 | 端點 | 說明 |
|------|------|------|
| POST | `/sentiments` | 新增情緒資料 |
| GET | `/sentiments` | 取得情緒列表 |
| GET | `/export/sentiments` | 匯出所有情緒資料 |

### GPS Coordinates（GPS 座標）
| 方法 | 端點 | 說明 |
|------|------|------|
| POST | `/gps` | 新增 GPS 座標 |
| GET | `/gps` | 取得 GPS 列表 |
| GET | `/export/gps` | 匯出所有 GPS 資料 |

---

## 📦 專案結構

```
emogo-backend/
├── main.py              # FastAPI 主程式（包含 HTML Dashboard）
├── requirements.txt     # Python 依賴套件
├── render.yaml          # Render 部署設定
├── .gitignore          # Git 忽略檔案
└── README.md           # 專案說明文件（本檔案）
└── cursor_emobackend_chat.md
```



---

## 📄 授權

此專案為課程作業，僅供學習使用。
