#!/usr/bin/env python3
"""
preview.py -- see the real site, on this machine, before it goes anywhere.

    python3 migration/preview.py

Builds dist/ exactly as the deploy does, then serves it at
http://localhost:8000 and prints every route. Ctrl-C to stop.

WHY THIS EXISTS
---------------
Opening a *-preview.html file straight off the disk does not show you the
site. It shows you the page with its images still pointing at
static.wixstatic.com, because the .dc.html sources reference Wix URLs on
purpose -- that is what lets migration/build-site.py find them and rewrite
them to /assets/. Two things then go wrong, and both of them look like a
design problem rather than a preview problem:

  1. THE LOGO IS A WIX IMAGE. When it does not load, the header renders as
     an almost-empty bar and the footer loses its mark, and the page reads
     as though the header and footer are missing. They are not. They are
     baked into every bundle -- see below.
  2. Any photograph on the page goes with it.

Anything that blocks that request does this: being offline, a content
blocker, a corporate proxy, or Wix itself once the subscription lapses.
That last one is the point of the whole migration, so the honest preview is
the built one, where nothing is loaded from Wix at all.

    --local  is what build-site.py calls the rewrite, and this script always
             passes it. It refuses to build if a single asset is missing,
             rather than shipping a site with holes in it.

ON HEADERS AND FOOTERS
----------------------
Nothing is added at hosting. There is no site-level chrome on Cloudflare or
Vercel the way there was on Wix -- every page is a standalone HTML file that
loads one bundle, and PtNav v3 and PtFooter v3 are compiled INTO that
bundle. That is why the README says to switch the Wix Header and Footer OFF
for every row in the table: leave them on and the page renders two navs and
two footers. What you see here is what deploys.
"""
import http.server, socketserver, subprocess, sys, pathlib, webbrowser, functools

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
DIST = REPO / "dist"
PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    """Serve dist/ with clean URLs, the way Cloudflare Pages does.

    /contact-daniel-lawson has no .html on the end and is a directory holding
    an index.html, which SimpleHTTPRequestHandler handles -- but only if the
    trailing slash is right. This fills in the gap so the URLs you test are
    the URLs that ship."""

    def do_GET(self):
        p = self.path.split("?")[0]
        candidate = DIST / p.lstrip("/")
        if p != "/" and candidate.is_dir() and (candidate / "index.html").exists():
            self.path = p.rstrip("/") + "/index.html"
        return super().do_GET()

    def log_message(self, fmt, *args):
        code = args[1] if len(args) > 1 else ""
        if str(code).startswith(("4", "5")):
            print("  %s %s" % (code, args[0]))


def main():
    print("Building dist/ ...\n")
    r = subprocess.run([sys.executable, str(HERE / "build-site.py"), "--local"],
                       cwd=str(REPO))
    if r.returncode != 0:
        print("\nBuild failed. Nothing served.")
        return r.returncode
    if not DIST.exists():
        print("\nNo dist/ directory after the build. Nothing served.")
        return 1

    routes = sorted(
        "/" + p.parent.relative_to(DIST).as_posix().rstrip(".")
        for p in DIST.glob("*/index.html")
    )
    print("\n" + "=" * 60)
    print("  http://localhost:%d/" % PORT)
    for rt in routes:
        print("  http://localhost:%d%s" % (PORT, rt))
    print("=" * 60)
    print("\nEverything above is served from your own machine with no Wix in it.")
    print("Ctrl-C to stop.\n")

    handler = functools.partial(Handler, directory=str(DIST))
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
            try:
                webbrowser.open("http://localhost:%d/contact-daniel-lawson" % PORT)
            except Exception:
                pass
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    except OSError as e:
        print("\nCould not bind port %d: %s" % (PORT, e))
        print("Something else is probably using it. Close it, or edit PORT above.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
