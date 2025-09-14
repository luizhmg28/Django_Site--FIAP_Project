import requests
import base64
import json
from typing import Dict

BASE = {
    "us": "https://us.semsportal.com",
    "eu": "https://eu.semsportal.com",
}

def _initial_token() -> str:
    original = {"uid": "", "timestamp": 0, "token": "", "client": "web", "version": "", "language": "en"}
    b = json.dumps(original).encode("utf-8")
    return base64.b64encode(b).decode("utf-8")

def crosslogin(account: str, password: str, region: str = "us") -> str:
    url = f"{BASE[region]}/api/v2/common/crosslogin"
    headers = {"Token": _initial_token(), "Content-Type": "application/json", "Accept": "*/*"}
    payload = {
        "account": account,
        "pwd": password,
        "agreement_agreement": 0,
        "is_local": False
    }
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    resp = r.json()
    if "data" not in resp or resp.get("code") not in (0, 1, 200):
        raise RuntimeError(f"Login falhou: {resp}")
    return base64.b64encode(json.dumps(resp["data"]).encode("utf-8")).decode("utf-8")

def get_inverter_data(token: str, inverter_sn: str, column: str, date: str, region: str = "eu") -> Dict:
    url = f"{BASE[region]}/api/PowerStationMonitor/GetInverterDataByColumn"
    headers = {"Token": token, "Content-Type": "application/json", "Accept": "*/*"}
    payload = {"id": inverter_sn, "column": column, "date": date}
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()
