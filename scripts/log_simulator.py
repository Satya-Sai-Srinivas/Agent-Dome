import time
import random
import json
import urllib.request

API_ENDPOINT = "http://localhost:8000/ingest"

# Mock data
IP_ADDRESSES = ["192.168.1.1", "10.0.0.5", "172.16.0.10", "203.0.113.5"]
ENDPOINTS = ["/login", "/dashboard", "/api/v1/users", "/home"]
ATTACKS = ["' OR 1=1 --", "<script>alert(1)</script>", "DROP TABLE users;", "../../../etc/passwd"]

def generate_log():
    is_attack = random.random() < 0.05  # 5% chance
    return {
        "timestamp": time.time(),
        "ip_address": random.choice(IP_ADDRESSES),
        "method": "POST" if is_attack else "GET",
        "endpoint": random.choice(ENDPOINTS),
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "payload": random.choice(ATTACKS) if is_attack else ""
    }

if __name__ == "__main__":
    print("🚀 Starting Log Simulator... Press Ctrl+C to stop.")
    while True:
        log = generate_log()
        data = json.dumps(log).encode('utf-8')
        req = urllib.request.Request(API_ENDPOINT, data=data, headers={'Content-Type': 'application/json'})
        try:
            urllib.request.urlopen(req)
            status = "🚨 ATTACK" if log["payload"] else "✅ CLEAN"
            print(f"Sent {status} from {log['ip_address']}")
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(random.uniform(0.5, 1.5))