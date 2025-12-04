# ⚡ 快速開始指南

## 📋 作業檢查清單

在繳交作業前，請確認以下項目：

- [ ] **MongoDB Atlas 已設定**
  - 建立了免費的 MongoDB Cluster
  - IP 白名單設為 `0.0.0.0/0`
  - 已取得連接字串

- [ ] **程式碼已推送到 GitHub**
  - 所有檔案都已 commit
  - 已 push 到 GitHub Classroom repository

- [ ] **已部署到 Render**
  - Web Service 已建立並成功部署
  - 環境變數已設定（MONGODB_URI, DB_NAME）
  - 可以訪問公開 URL

- [ ] **README.md 已更新**
  - 包含三個資料匯出端點的完整 URL
  - URL 已替換為實際的 Render URL

- [ ] **API 端點可正常運作**
  - `/export/vlogs` 可訪問
  - `/export/sentiments` 可訪問
  - `/export/gps` 可訪問

- [ ] **已繳交到 NTU COOL**
  - 繳交 GitHub repository URL
  - 在 12/4（四）晚上 8:00 前完成

---

## 🎯 三個關鍵 URL（作業要求）

**請在部署後，將以下 URL 更新到 README.md：**

1. **Vlogs 匯出**  
   `https://your-app-name.onrender.com/export/vlogs`

2. **Sentiments 匯出**  
   `https://your-app-name.onrender.com/export/sentiments`

3. **GPS Coordinates 匯出**  
   `https://your-app-name.onrender.com/export/gps`

---

## 🚀 三步驟完成部署

### 1️⃣ MongoDB Atlas（5 分鐘）
```
1. 註冊 → mongodb.com/cloud/atlas
2. 建立免費 Cluster
3. 設定 IP: 0.0.0.0/0
4. 建立使用者並取得連接字串
```

### 2️⃣ 推送到 GitHub（1 分鐘）
```bash
git add .
git commit -m "Complete EmoGo Backend"
git push
```

### 3️⃣ 部署到 Render（10 分鐘）
```
1. 登入 render.com
2. New Web Service → 選擇你的 repo
3. 設定環境變數：
   - MONGODB_URI: 你的連接字串
   - DB_NAME: emogo_db
4. Create Web Service
5. 等待部署完成
```

---

## 🧪 快速測試

**測試 API 是否正常運作：**

```bash
# 使用測試腳本
python test_api.py https://your-app-name.onrender.com

# 或在瀏覽器中開啟
https://your-app-name.onrender.com/docs
```

**手動測試資料匯出端點：**

在瀏覽器中開啟這三個網址，應該會看到 JSON 資料：
- `https://your-app-name.onrender.com/export/vlogs`
- `https://your-app-name.onrender.com/export/sentiments`
- `https://your-app-name.onrender.com/export/gps`

---

## 📊 專案架構

```
emogo-backend/
├── main.py              # 主程式 - FastAPI + MongoDB
├── requirements.txt     # Python 套件依賴
├── render.yaml          # Render 部署設定
├── test_api.py          # API 測試腳本
├── README.md            # 專案說明（包含匯出 URI）
├── DEPLOYMENT_GUIDE.md  # 詳細部署指南
├── QUICK_START.md       # 快速開始指南（本檔案）
└── .gitignore          # Git 忽略檔案
```

---

## 💡 重要提醒

1. **環境變數**：在 Render 上必須設定 `MONGODB_URI` 和 `DB_NAME`
2. **IP 白名單**：MongoDB Atlas 必須設為 `0.0.0.0/0`
3. **README 更新**：記得將 `your-app-name` 替換為實際的 Render URL
4. **測試資料**：可以使用 MongoDB Compass 或 API 文件新增測試資料
5. **免費方案**：Render 免費方案在閒置 15 分鐘後會休眠，首次訪問需要等待啟動

---

## 📞 需要幫助？

詳細部署步驟請參考：[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

**Good Luck! 🎓**

