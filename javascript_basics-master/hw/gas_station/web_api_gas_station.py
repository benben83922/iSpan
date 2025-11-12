'''
請先安裝:
pip install flask flask-cors requests

資料來源:
[1] 臺北市資料大平臺
https://data.taipei/
[2] YouBike2.0臺北市公共自行車即時資訊
https://data.taipei/dataset/detail?id=c6bc8aed-557d-41d5-bfb1-8da24f78f2fb
[3] 介接網址
https://vipmbr.cpc.com.tw/opendata/5typeservicestn
'''

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from urllib.parse import quote_plus
import requests, uuid
from pathlib import Path

# 建立 Flask 伺服器
app = Flask(__name__)

# 自動處理 CORS
CORS(app)

# Web API
URL = "https://vipmbr.cpc.com.tw/opendata/5typeservicestn"

# 請求標頭
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/142.0.0.0 Safari/537.36"
}

# 自訂路由端點 (Route Endpoint)
@app.route("/gas_station", methods=["GET"])
def gas_station():
    # 請求資料
    r = requests.get(URL, headers=HEADERS, timeout=10, verify=False)

    # 轉換回應為 JSON 格式 (將字串轉為類似 Object/Dict 的格式)
    resp = jsonify(r.json())

    # 回傳結果
    return resp


# 主程式
if __name__ == "__main__":
    # 開發測試用
    app.run(
        host="0.0.0.0", # 允許外部存取
        port=5000, # 服務 port 號
        debug=True # 除錯模式 (開發時使用，正式上線請移除或設為 False)
    )
