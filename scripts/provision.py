#!/usr/bin/env python3
"""CTFd challenge provisioner for mobsec-ctf-lab.

Connects to a running CTFd and, using the public web + JSON API, performs
first-time setup (creates the admin) and provisions every challenge defined in
challenges/challenges.json (categories, descriptions, points, hints, flags).

Idempotent: existing challenges (matched by name) are skipped.

Browsing/API notes:
  - CTFd setup and login are CSRF-protected web forms; the JSON API carries a
    CSRF nonce that this script extracts from the page's `init.csrfNonce`.
  - Uses only the Python standard library (runs in a disposable container).

Configuration via environment:
  CTFD_URL            (default http://ctfd:8000)
  CTFD_ADMIN_EMAIL / CTFD_ADMIN_PASSWORD
  CTFD_CTF_NAME / CTFD_CTF_DESCRIPTION / CTFD_MODE
  CHALLENGES_FILE     (default challenges/challenges.json)
"""

import http.cookiejar
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urlencode

CTFD_URL = os.environ.get("CTFD_URL", "http://ctfd:8000").rstrip("/")
ADMIN_EMAIL = os.environ.get("CTFD_ADMIN_EMAIL", "instructor@lab.local")
ADMIN_PASSWORD = os.environ.get("CTFD_ADMIN_PASSWORD", "ChangeMe-Admin-2026")
CTF_NAME = os.environ.get("CTFD_CTF_NAME", "Mobile Security CTF Lab")
CTF_DESCRIPTION = os.environ.get("CTFD_CTF_DESCRIPTION", "Local mobile app security course lab")
MODE = os.environ.get("CTFD_MODE", "teams")
CHALLENGES_FILE = os.environ.get("CHALLENGES_FILE", "challenges/challenges.json")

_cj = http.cookiejar.CookieJar()
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_cj))


def _http(method, path, body=None, form=False, csrf=None, timeout=40):
    headers = {"Accept": "application/json"}
    if csrf:
        headers["CSRF-Token"] = csrf
    if body is None:
        payload = None
    elif form:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        payload = urlencode(body).encode()
    else:
        headers["Content-Type"] = "application/json"
        payload = json.dumps(body).encode()
    req = urllib.request.Request(CTFD_URL + path, data=payload, headers=headers, method=method)
    try:
        with _opener.open(req, timeout=timeout) as resp:
            raw = resp.read()
            final_url = resp.geturl()
            try:
                return resp.status, json.loads(raw), final_url
            except Exception:
                return resp.status, raw.decode(errors="replace"), final_url
    except urllib.error.HTTPError as e:
        raw = e.read()
        final_url = e.geturl()
        try:
            return e.code, json.loads(raw), final_url
        except Exception:
            return e.code, raw.decode(errors="replace"), final_url


def _form_nonce(path="/setup"):
    status, body, _ = _http("GET", path)
    if isinstance(body, str):
        m = re.search(r'name="nonce"[^>]*value="([^"]+)"', body)
        return m.group(1) if m else None
    return None


def _js_nonce(path="/challenges"):
    status, body, _ = _http("GET", path)
    if isinstance(body, str):
        m = re.search(r"'csrfNonce':\s*\"([^\"]+)\"", body)
        return m.group(1) if m else None
    return None


def wait_ready(retries=90, delay=5):
    for i in range(retries):
        status, _, _ = _http("GET", "/api/v1/challenges")
        if status == 200:
            return True
        if status in (302, 401, 403):
            return True
        print(f"[wait] CTFd not ready ({status}); {i + 1}/{retries}")
        time.sleep(delay)
    raise SystemExit("CTFd did not become ready in time.")


def _is_setup_done():
    # A configured CTFd redirects GET /setup away from the setup form (to /
    # or /login). An unconfigured CTFd serves the setup form at /setup.
    if not _setup_form_present():
        return True
    return False


def _setup_form_present():
    # urllib follows redirects; if we end up at /setup with the form, it's
    # not configured yet.
    status, body, _ = _http("GET", "/setup")
    if isinstance(body, str) and 'name="ctf_name"' in body:
        return True
    return False


def ensure_setup():
    if _is_setup_done():
        print("[setup] CTFd already configured; skipping setup.")
        return
    for attempt in range(5):
        nonce = _form_nonce("/setup")
        status, body, _ = _http(
            "POST",
            "/setup",
            form=True,
            body={
                "nonce": nonce,
                "ctf_name": CTF_NAME,
                "ctf_description": CTF_DESCRIPTION,
                "user_mode": MODE,
                "name": ADMIN_EMAIL.split("@")[0],
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD,
                "confirm": ADMIN_PASSWORD,
            },
        )
        if _is_setup_done():
            print("[setup] CTFd configured; admin created.")
            return
        time.sleep(2)
    raise SystemExit("[setup] Failed to set up CTFd.")


def login():
    for attempt in range(5):
        nonce = _form_nonce("/login")
        status, body, _ = _http(
            "POST",
            "/login",
            form=True,
            body={"nonce": nonce, "name": ADMIN_EMAIL.split("@")[0],
                  "password": ADMIN_PASSWORD},
        )
        csrf = _js_nonce("/challenges")
        if csrf:
            return csrf
        time.sleep(2)
    raise SystemExit("[login] Could not authenticate to CTFd.")


def existing_challenges():
    status, body, _ = _http("GET", "/api/v1/challenges")
    return body.get("data", []) if isinstance(body, dict) else []


def create_challenge(csrf, ch):
    payload = {
        "name": ch["name"],
        "category": ch["category"],
        "value": ch["value"],
        "type": "standard",
        "description": ch["description"],
        "state": "visible",
    }
    status, body, _ = _http("POST", "/api/v1/challenges", body=payload, csrf=csrf)
    if status not in (200, 201):
        raise SystemExit(f"[create] {ch['name']}: {status} {body}")
    cid = body["data"]["id"]
    print(f"[create] '{ch['name']}' (id={cid})")
    return cid


def add_flag(csrf, cid, flag):
    payload = {"challenge_id": cid, "content": flag, "type": "static",
               "data": "case_insensitive"}
    status, body, _ = _http("POST", "/api/v1/flags", body=payload, csrf=csrf)
    if status not in (200, 201):
        raise SystemExit(f"[flag] {status} {body}")


def add_hints(csrf, cid, hints):
    for h in hints:
        payload = {"challenge_id": cid, "content": h, "cost": 0}
        status, body, _ = _http("POST", "/api/v1/hints", body=payload, csrf=csrf)
        if status not in (200, 201):
            raise SystemExit(f"[hint] {status} {body}")


def main():
    wait_ready()
    ensure_setup()
    csrf = login()
    with open(CHALLENGES_FILE, encoding="utf-8") as f:
        reg = json.load(f)

    seen = {c["name"] for c in existing_challenges()}
    for ch in reg["challenges"]:
        if ch["name"] in seen:
            print(f"[skip] '{ch['name']}' already exists.")
            continue
        cid = create_challenge(csrf, ch)
        add_flag(csrf, cid, ch["flag"])
        add_hints(csrf, cid, ch.get("hints", []))

    print("[done] Challenge provisioning complete.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        print(e)
        sys.exit(1)