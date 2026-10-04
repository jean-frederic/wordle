import urllib.request
import json
import threading
import time
from web_server import HTTPServer, WordleRequestHandler

server = HTTPServer(('127.0.0.1', 8999), WordleRequestHandler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()

time.sleep(0.5)

# Test 1: GET /api/init
req = urllib.request.urlopen('http://127.0.0.1:8999/api/init')
data = json.loads(req.read().decode('utf-8'))
print("API /api/init response:")
print("  Total targets:", data["total_targets"])
print("  Total allowed:", data["total_allowed"])
print("  Today word:", data["today_word"])
print("  Top opener:", data["recommended_openers"][0]["word"])

# Test 2: POST /api/analyze with first guess TARIE -> [0, 0, 0, 0, 0] (all grey)
payload = json.dumps({
    "history": [
        {"guess": "TARIE", "pattern": [0, 0, 0, 0, 0]}
    ]
}).encode('utf-8')
req2 = urllib.request.Request(
    'http://127.0.0.1:8999/api/analyze',
    data=payload,
    headers={'Content-Type': 'application/json'}
)
resp2 = urllib.request.urlopen(req2)
data2 = json.loads(resp2.read().decode('utf-8'))
print("\nAPI /api/analyze response (TARIE all grey):")
print("  Remaining count:", data2["remaining_count"])
print("  Top suggestion:", data2["suggestions"][0]["word"], "reason:", data2["suggestions"][0]["reason"])

server.shutdown()
print("\nServer API verified successfully!")
