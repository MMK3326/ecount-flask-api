from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

EC_API_URL = "https://secure.ecount.com/OpenAPI/OpenApiRequest.aspx"
API_KEY = os.getenv("EC_API_KEY")
COMPANY_CODE = os.getenv("EC_COMPANY_CODE")
USER_ID = os.getenv("EC_USER_ID")
USER_PW = os.getenv("EC_USER_PW")

@app.route("/")
def home():
    return "ECOUNT Flask API 서버가 정상적으로 작동 중입니다 ✅"

@app.route("/stock-in", methods=["POST"])
def stock_in():
    data = request.json
    payload = {
        "APIKey": API_KEY,
        "ClientCode": COMPANY_CODE,
        "UserID": USER_ID,
        "Password": USER_PW,
        "APIName": "입고등록",
        "Parameter": {
            "입고일": data.get("date", "2025-04-17"),
            "품목코드": data["item_code"],
            "수량": data["qty"],
            "창고코드": data["warehouse_code"],
            "입고유형": "정상"
        }
    }
    res = requests.post(EC_API_URL, json=payload)
    return jsonify(res.json())

@app.route("/stock-status", methods=["GET"])
def stock_status():
    warehouse_code = request.args.get("warehouse", "")
    payload = {
        "APIKey": API_KEY,
        "ClientCode": COMPANY_CODE,
        "UserID": USER_ID,
        "Password": USER_PW,
        "APIName": "재고현황",
        "Parameter": {
            "조회일": "2025-04-17",
            "창고": warehouse_code
        }
    }
    res = requests.post(EC_API_URL, json=payload)
    return jsonify(res.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
