import os
import sys
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
from wordle_engine import WordleEngine

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

engine = WordleEngine()
PORT = 8765

class WordleRequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.serve_file("index.html", "text/html; charset=utf-8")
        elif path == "/api/init":
            today_word, today_date = engine.get_louan_daily_word()
            data = {
                "total_targets": len(engine.target_words),
                "total_allowed": len(engine.all_words),
                "recommended_openers": engine.recommended_openers,
                "today_word": today_word,
                "today_date": today_date
            }
            self.send_json(data)
        elif path == "/api/oracle":
            date_param = query.get("date", [None])[0]
            word, dt = engine.get_louan_daily_word(date_param)
            self.send_json({"date": dt, "word": word})
        elif path == "/api/plan":
            target = query.get("word", [None])[0]
            mode = int(query.get("mode", [2])[0])
            if not target:
                self.send_json({"error": "Parametre 'word' requis"}, status=400)
                return
            try:
                plan = engine.generate_guaranteed_plan(target, mode=mode)
                self.send_json({"target": target, "mode": mode, "plan": plan})
            except Exception as e:
                self.send_json({"error": str(e)}, status=400)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/analyze":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                req_data = json.loads(body)
                history = req_data.get("history", [])
                
                candidates = engine.target_words[:]
                
                for step in history:
                    guess = step.get("guess", "").upper().strip()
                    pattern = step.get("pattern", [])
                    if len(guess) == 5 and len(pattern) == 5:
                        p_int = 0
                        for v in pattern:
                            p_int = p_int * 3 + int(v)
                        candidates = engine.filter_candidates(candidates, guess, p_int)
                
                suggestions = engine.analyze_suggestions(candidates, top_n=6)
                
                self.send_json({
                    "remaining_count": len(candidates),
                    "candidates": candidates[:60],
                    "has_more": len(candidates) > 60,
                    "suggestions": suggestions
                })
            except Exception as e:
                self.send_json({"error": str(e)}, status=400)
        else:
            self.send_response(404)
            self.end_headers()

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def serve_file(self, filename, content_type):
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        if not os.path.exists(filepath):
            self.send_response(404)
            self.end_headers()
            return
        with open(filepath, 'rb') as f:
            content = f.read()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

def start_server(port=PORT, open_browser=True):
    server = HTTPServer(('127.0.0.1', port), WordleRequestHandler)
    url = f"http://127.0.0.1:{port}"
    print(f"\nServeur Wordle Puzzle Solver pret sur {url}")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArret du serveur...")
        server.server_close()

if __name__ == "__main__":
    start_server()
