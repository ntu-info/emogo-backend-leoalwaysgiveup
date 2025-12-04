#!/usr/bin/env python3
"""
EmoGo Backend API 測試腳本

使用方式:
1. 本地測試: python test_api.py http://localhost:8000
2. 遠端測試: python test_api.py https://your-app.onrender.com
"""

import requests
import json
import sys
from datetime import datetime

def test_api(base_url):
    """測試 EmoGo Backend API 的所有功能"""
    
    print(f"🧪 開始測試 EmoGo Backend API")
    print(f"📡 URL: {base_url}\n")
    
    # 測試首頁
    print("1️⃣ 測試首頁...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   ✅ 狀態碼: {response.status_code}")
        print(f"   📄 回應: {response.json()}\n")
    except Exception as e:
        print(f"   ❌ 錯誤: {e}\n")
        return
    
    # 測試健康檢查
    print("2️⃣ 測試健康檢查...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   ✅ 狀態碼: {response.status_code}")
        print(f"   📄 回應: {response.json()}\n")
    except Exception as e:
        print(f"   ❌ 錯誤: {e}\n")
    
    # 測試新增情緒資料
    print("3️⃣ 測試新增情緒資料...")
    sentiment_data = {
        "user_id": "test_user_001",
        "emotion": "happy",
        "intensity": 0.85,
        "note": "測試資料 - 今天天氣很好！",
        "timestamp": datetime.now().isoformat()
    }
    try:
        response = requests.post(
            f"{base_url}/sentiments",
            json=sentiment_data
        )
        print(f"   ✅ 狀態碼: {response.status_code}")
        print(f"   📄 回應: {response.json()}\n")
    except Exception as e:
        print(f"   ❌ 錯誤: {e}\n")
    
    # 測試新增 GPS 座標
    print("4️⃣ 測試新增 GPS 座標...")
    gps_data = {
        "user_id": "test_user_001",
        "latitude": 25.0330,
        "longitude": 121.5654,
        "accuracy": 10.5,
        "timestamp": datetime.now().isoformat()
    }
    try:
        response = requests.post(
            f"{base_url}/gps",
            json=gps_data
        )
        print(f"   ✅ 狀態碼: {response.status_code}")
        print(f"   📄 回應: {response.json()}\n")
    except Exception as e:
        print(f"   ❌ 錯誤: {e}\n")
    
    # 測試新增影片日誌
    print("5️⃣ 測試新增影片日誌...")
    vlog_data = {
        "user_id": "test_user_001",
        "title": "測試影片日誌",
        "description": "這是一個測試用的影片日誌",
        "video_url": "https://example.com/test_video.mp4",
        "duration": 120.5,
        "timestamp": datetime.now().isoformat()
    }
    try:
        response = requests.post(
            f"{base_url}/vlogs",
            json=vlog_data
        )
        print(f"   ✅ 狀態碼: {response.status_code}")
        print(f"   📄 回應: {response.json()}\n")
    except Exception as e:
        print(f"   ❌ 錯誤: {e}\n")
    
    # 測試統計資訊
    print("6️⃣ 測試統計資訊...")
    try:
        response = requests.get(f"{base_url}/stats")
        print(f"   ✅ 狀態碼: {response.status_code}")
        print(f"   📊 統計: {response.json()}\n")
    except Exception as e:
        print(f"   ❌ 錯誤: {e}\n")
    
    # 測試匯出資料
    print("7️⃣ 測試匯出情緒資料...")
    try:
        response = requests.get(f"{base_url}/export/sentiments")
        data = response.json()
        print(f"   ✅ 狀態碼: {response.status_code}")
        print(f"   📦 資料數量: {data.get('total_count', 0)}\n")
    except Exception as e:
        print(f"   ❌ 錯誤: {e}\n")
    
    print("8️⃣ 測試匯出 GPS 座標...")
    try:
        response = requests.get(f"{base_url}/export/gps")
        data = response.json()
        print(f"   ✅ 狀態碼: {response.status_code}")
        print(f"   📦 資料數量: {data.get('total_count', 0)}\n")
    except Exception as e:
        print(f"   ❌ 錯誤: {e}\n")
    
    print("9️⃣ 測試匯出影片日誌...")
    try:
        response = requests.get(f"{base_url}/export/vlogs")
        data = response.json()
        print(f"   ✅ 狀態碼: {response.status_code}")
        print(f"   📦 資料數量: {data.get('total_count', 0)}\n")
    except Exception as e:
        print(f"   ❌ 錯誤: {e}\n")
    
    print("=" * 50)
    print("✅ 測試完成！")
    print("=" * 50)
    print("\n📚 請在瀏覽器中開啟以下網址查看完整 API 文件：")
    print(f"   {base_url}/docs\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方式: python test_api.py <BASE_URL>")
        print("範例:")
        print("  python test_api.py http://localhost:8000")
        print("  python test_api.py https://your-app.onrender.com")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    test_api(base_url)

