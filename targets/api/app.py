"""GlowMart Mobile API - intentionally simple backend for the mobile lab.

EDUCATIONAL LAB TARGET ONLY. Never expose to the internet.

Serves two endpoints:
  - HTTP  :3000      plain endpoints the emulator calls (session, health)
  - HTTPS :3443      pinned-TLS endpoint (Module 3 SSL-pinning lab). The
                     certificate is committed in certs/ and the app pins its
                     SPKI hash; interception is only possible after the app's
                     pinning check is bypassed (Frida).
"""

import json
import ssl
import threading

from flask import Flask, jsonify

app = Flask(__name__)

CERT = "/app/certs/server.crt"
KEY = "/app/certs/server.key"

BANNER = {
    "service": "glowmart-mobile-api",
    "version": "1.3.0",
    "env": "production",
    "flag": "flag{ssl_pinning_bypassed}",
    "note": ("This endpoint is normally reachable only through the app's "
             "pinned TLS channel. You are seeing it because the pin was "
             "bypassed (Frida) and/or the traffic was intercepted."),
}


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/v1/mobile/session")
def session():
    return jsonify({"ok": True, "session": "glotest", "ttl": 3600})


@app.route("/api/v1/mobile/banner")
def banner():
    return jsonify(BANNER)


def serve_http():
    app.run(host="0.0.0.0", port=3000, debug=False, use_reloader=False)


def serve_https():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT, KEY)
    app.run(host="0.0.0.0", port=3443, ssl_context=ctx,
            debug=False, use_reloader=False)


if __name__ == "__main__":
    t_http = threading.Thread(target=serve_http, daemon=True)
    t_https = threading.Thread(target=serve_https, daemon=True)
    t_http.start()
    t_https.start()
    t_http.join()
    t_https.join()