"""HTTP API and privacy-conscious request tracing for Rafeeq."""
import json
import logging
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from main import Rafeeq

HOST = "127.0.0.1"
PORT = 8000
agent = Rafeeq()

logging.basicConfig(
    filename="traces.log",
    level=logging.INFO,
    format="%(message)s",
)
logger = logging.getLogger("rafeeq.traces")


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ok", "service": "Rafeeq"})
        else:
            self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/chat":
            self.send_json(404, {"error": "Not found"})
            return

        trace_id = str(uuid.uuid4())
        started = time.perf_counter()
        status = 200

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 100_000:
                self.send_json(400, {"error": "Invalid request size"})
                status = 400
                return

            data = json.loads(self.rfile.read(length))
            message = data.get("message")
            language = data.get("language", "en")

            if not isinstance(message, str) or not message.strip():
                self.send_json(400, {"error": "message must be a non-empty string"})
                status = 400
                return

            if language not in ("en", "ar"):
                self.send_json(400, {"error": "language must be en or ar"})
                status = 400
                return

            result = agent.respond(message, language=language)
            self.send_json(200, {
                "trace_id": trace_id,
                **result,
            })

        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            status = 400
            self.send_json(400, {"error": "Invalid JSON request"})
        except Exception:
            status = 500
            self.send_json(500, {
                "trace_id": trace_id,
                "error": "Internal server error",
            })
        finally:
            logger.info(json.dumps({
                "trace_id": trace_id,
                "method": "POST",
                "path": self.path,
                "status": status,
                "duration_ms": round(
                    (time.perf_counter() - started) * 1000, 2
                ),
                "timestamp": time.time(),
            }))

    def log_message(self, format, *args):
        # Avoid logging request content or other unnecessary details.
        pass


if __name__ == "__main__":
    print(f"Rafeeq API running at http://{HOST}:{PORT}")
    print("Endpoints: GET /health, POST /chat")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
