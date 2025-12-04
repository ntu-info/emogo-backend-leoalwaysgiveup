# 🚀 EmoGo Backend 部署指南

## 完整部署步驟

### 第一步：設定 MongoDB Atlas

1. **註冊 MongoDB Atlas**
   - 前往 https://www.mongodb.com/cloud/atlas
   - 註冊免費帳號
   - 建立一個新的 Cluster（選擇免費方案 M0）

2. **設定網路存取**
   - 點選左側選單 **Security > Network Access**
   - 點選 **Add IP Address**
   - 選擇 **Allow Access from Anywhere**
   - 輸入 IP: `0.0.0.0/0`
   - 點選 **Confirm**

3. **建立資料庫使用者**
   - 點選左側選單 **Security > Database Access**
   - 點選 **Add New Database User**
   - 選擇 **Password** 驗證方式
   - 輸入使用者名稱和密碼（記下這些資訊！）
   - 選擇權限：**Read and write to any database**
   - 點選 **Add User**

4. **取得連接字串**
   - 點選左側選單 **Data Services > Database**
   - 點選你的 Cluster 的 **Connect** 按鈕
   - 選擇 **Connect your application**
   - 選擇 Driver: **Python**, Version: **3.12 or later**
   - 複製連接字串，格式如：
     ```
     mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
     ```
   - **重要**：將 `<password>` 替換為你剛才設定的密碼

5. **（選用）使用 MongoDB Compass 建立測試資料**
   - 下載並安裝 [MongoDB Compass](https://www.mongodb.com/products/compass)
   - 使用連接字串連接到你的資料庫
   - 建立資料庫 `emogo_db`
   - 建立三個 collections：`vlogs`、`sentiments`、`gps_coordinates`
   - 手動新增一些測試資料

---

### 第二步：推送程式碼到 GitHub

1. **初始化 Git（如果還沒有）**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: EmoGo Backend"
   ```

2. **連接到 GitHub Repository**
   - 這個作業應該已經是從 GitHub Classroom 建立的
   - 如果還沒推送，執行：
   ```bash
   git remote add origin https://github.com/your-username/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

---

### 第三步：部署到 Render

1. **登入 Render**
   - 前往 https://render.com/
   - 使用 GitHub 帳號登入

2. **建立新的 Web Service**
   - 點選右上角 **New +**
   - 選擇 **Web Service**
   - 點選 **Connect a repository**
   - 選擇你的 GitHub repository（可能需要授權 Render 存取）

3. **設定 Web Service**
   - **Name**: 輸入一個名稱，例如 `emogo-backend-yourname`
   - **Region**: 選擇離你最近的區域（例如：Singapore）
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

4. **設定環境變數**
   - 往下滾動到 **Environment Variables** 區域
   - 點選 **Add Environment Variable**
   - 新增以下兩個變數：
   
   **變數 1:**
   - Key: `MONGODB_URI`
   - Value: 你的 MongoDB 連接字串（例如：`mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/`）
   
   **變數 2:**
   - Key: `DB_NAME`
   - Value: `emogo_db`

5. **建立服務**
   - 檢查所有設定無誤
   - 點選 **Create Web Service**
   - 等待部署完成（約 3-5 分鐘）

6. **取得你的 URL**
   - 部署完成後，你會看到一個 URL，例如：
     ```
     https://emogo-backend-yourname.onrender.com
     ```
   - 這就是你的公開網址！

---

### 第四步：測試你的 API

1. **開啟 API 文件**
   - 在瀏覽器中開啟：
     ```
     https://your-app-name.onrender.com/docs
     ```

2. **測試首頁**
   - 開啟：
     ```
     https://your-app-name.onrender.com/
     ```
   - 應該會看到 API 資訊

3. **使用測試腳本**
   - 在本地執行：
   ```bash
   python test_api.py https://your-app-name.onrender.com
   ```

4. **測試資料匯出端點（作業要求！）**
   - 在瀏覽器中開啟以下網址：
     ```
     https://your-app-name.onrender.com/export/vlogs
     https://your-app-name.onrender.com/export/sentiments
     https://your-app-name.onrender.com/export/gps
     ```
   - 應該會看到 JSON 格式的資料

---

### 第五步：更新 README.md

1. **編輯 README.md**
   - 找到 `your-app-name.onrender.com` 的部分
   - 替換為你的實際 URL

2. **推送變更到 GitHub**
   ```bash
   git add README.md
   git commit -m "Update README with deployment URL"
   git push
   ```

---

### 第六步：繳交作業

1. **確認以下項目**
   - [ ] MongoDB Atlas 已設定完成
   - [ ] 應用程式已部署到 Render
   - [ ] README.md 中包含資料匯出的 URI
   - [ ] 三個資料匯出端點都可以正常訪問
   - [ ] GitHub repository 是最新的

2. **繳交到 NTU COOL**
   - 前往 NTU COOL 課程頁面
   - 繳交你的 GitHub repository URL
   - 截止時間：**12/4（四）晚上 8:00**

---

## 常見問題解決

### Q1: Render 部署失敗
**A:** 檢查以下項目：
- `requirements.txt` 是否正確
- `Start Command` 是否為：`uvicorn main:app --host 0.0.0.0 --port $PORT`
- 環境變數是否設定正確

### Q2: 無法連接到 MongoDB
**A:** 檢查：
- MongoDB Atlas 的 IP 白名單是否設為 `0.0.0.0/0`
- 連接字串中的密碼是否正確（注意特殊字元需要 URL encode）
- 資料庫使用者權限是否足夠

### Q3: API 端點回應 500 錯誤
**A:** 
- 在 Render Dashboard 查看 Logs
- 檢查 MongoDB 連接字串是否正確
- 確認環境變數已設定

### Q4: Render 免費方案限制
**A:** 
- 免費方案在 15 分鐘無活動後會休眠
- 首次訪問可能需要等待 30 秒啟動
- 每月有 750 小時的免費使用時間

---

## 本地開發測試

如果你想在本地測試：

1. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

2. **設定環境變數**
   ```bash
   export MONGODB_URI="你的MongoDB連接字串"
   export DB_NAME="emogo_db"
   ```

3. **啟動伺服器**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **開啟瀏覽器**
   - http://localhost:8000/docs

---

## 需要協助？

- 查看 Render Logs：Dashboard > Logs
- 查看 MongoDB Atlas Metrics：Atlas > Metrics
- 課程討論區提問
- 聯絡助教

---

**祝你部署順利！🎉**

