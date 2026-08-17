#!/usr/bin/env python3
"""
serve.py — local preview server for dist/, with HTTP Range support.

WHY THIS EXISTS
---------------
`python3 -m http.server` does not implement Range requests: it answers every
request with 200 and the whole file. Chrome requires 206 partial responses to
play video, so on the plain server the player opens, spins, and never starts —
which looks exactly like a broken migration and is not one.

Cloudflare Pages supports Range, so this only affects local testing. But without
it you cannot judge the video quality, which is the whole point of previewing.

Also serves /the-reconnected-man from the-reconnected-man/index.html, matching
how Pages resolves clean URLs, so the preview routes behave like production.

    python3 migration/serve.py          # serves ../dist on :8000
    python3 migration/serve.py 8080     # different port
"""
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "dist")
ROOT = os.path.abspath(ROOT)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def handle_one_request(self):
        # Chrome routinely opens a range request, gets what it needs and hangs
        # up — seeking in a video does it, so does navigating away mid-load.
        # Python answers that with a BrokenPipeError and a twenty-line traceback
        # that reads like a crash. The request is already served; swallow it so
        # the console shows real problems only.
        try:
            super().handle_one_request()
        except (BrokenPipeError, ConnectionResetError):
            self.close_connection = True

    def log_message(self, fmt, *args):
        code = args[1] if len(args) > 1 else ""
        if str(code).startswith(("4", "5")):      # only surface problems
            super().log_message(fmt, *args)

    def translate_path(self, path):
        p = super().translate_path(path)
        # Clean URLs: /men -> /men/index.html, the way Pages resolves them.
        if not os.path.exists(p) and not os.path.splitext(p)[1]:
            cand = os.path.join(p, "index.html")
            if os.path.exists(cand):
                return cand
        return p

    def send_head(self):
        rng = self.headers.get("Range")
        if not rng:
            return super().send_head()

        path = self.translate_path(self.path)
        if os.path.isdir(path) or not os.path.exists(path):
            return super().send_head()

        m = re.match(r"bytes=(\d*)-(\d*)", rng)
        if not m:
            return super().send_head()

        size = os.path.getsize(path)
        start = int(m.group(1)) if m.group(1) else 0
        end = int(m.group(2)) if m.group(2) else size - 1
        end = min(end, size - 1)
        if start > end:
            self.send_error(416, "Requested Range Not Satisfiable")
            return None

        f = open(path, "rb")
        f.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()

        # Hand back a reader bounded to the requested slice.
        remaining = end - start + 1
        original_read = f.read

        def bounded(n=-1):
            nonlocal remaining
            if remaining <= 0:
                return b""
            chunk = original_read(min(n if n and n > 0 else remaining, remaining))
            remaining -= len(chunk)
            return chunk

        f.read = bounded
        return f


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    if not os.path.isdir(ROOT):
        sys.exit(f"No dist/ at {ROOT} — run build-site.py --local first.")
    print(f"serving {ROOT} with Range support on http://localhost:{port}")
    print("routes: /  /men  /women  /the-reconnected-man  /the-reconnected-woman")
    print("        /priority-audit  /about-daniel-lawson  /testimonials-daniel-lawson")
    print("        /the-archetype-quiz  /wheel-of-reconnect")
    print("Ctrl+C to stop.")
    ThreadingHTTPServer(("", port), Handler).serve_forever()
