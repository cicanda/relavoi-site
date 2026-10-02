#!/usr/bin/env python3
"""Verify every link on the site resolves.

Local pages and assets must exist on disk; in-page anchors must match a real
id; external URLs must return < 400. Run before every deploy:

    python3 check-links.py            # check the files in this directory
    python3 check-links.py --live     # also re-check against relavoi.com

Exits non-zero if anything is broken, so it can gate a deploy.
"""
import glob
import os
import re
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = sorted(glob.glob(os.path.join(HERE, "*.html")))
EXTRA_SOURCES = [os.path.join(HERE, "site.js")]
LIVE_ORIGIN = "https://relavoi.com"

# Skip resource hints — preconnect/dns-prefetch targets legitimately 404 on a GET.
HINT = re.compile(r'<link[^>]*rel="(?:preconnect|dns-prefetch)"[^>]*>')
HREF = re.compile(r'(?:href|src)="([^"]+)"')
ID = re.compile(r'\sid="([^"]+)"')


def ids_in(path):
    try:
        return set(ID.findall(open(path, encoding="utf-8").read()))
    except OSError:
        return set()


def head(url, timeout=15):
    """Return a status code, following redirects. HEAD, falling back to GET."""
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method,
                                     headers={"User-Agent": "relavoi-link-check"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue          # some hosts refuse HEAD; retry as GET
            return e.code
        except Exception as e:                     # DNS, TLS, timeout
            return f"ERR {type(e).__name__}"
    return "ERR"


def main():
    live = "--live" in sys.argv
    problems = []
    checked_remote = {}

    for src in PAGES + EXTRA_SOURCES:
        name = os.path.basename(src)
        try:
            body = open(src, encoding="utf-8").read()
        except OSError:
            continue
        for link in HREF.findall(HINT.sub("", body)):
            if "'+l[0]+'" in link:
                continue                            # template literal in site.js
            if link.startswith(("mailto:", "tel:", "data:")):
                continue
            if link.startswith(("http://", "https://")):
                if link not in checked_remote:
                    checked_remote[link] = head(link)
                status = checked_remote[link]
                if not (isinstance(status, int) and status < 400):
                    problems.append(f"{name}: {link} -> {status}")
            elif link.startswith("#"):
                if link != "#" and link[1:] not in ids_in(src):
                    problems.append(f"{name}: anchor {link} has no matching id")
                elif link == "#":
                    problems.append(f"{name}: dead placeholder href=\"#\"")
            else:
                path, _, frag = link.partition("#")
                target = os.path.join(HERE, path) if path else src
                if path and not os.path.exists(target):
                    problems.append(f"{name}: {path} does not exist")
                elif frag and frag not in ids_in(target):
                    problems.append(f"{name}: {link} -> no id '{frag}' in {path or name}")

    if live:
        for page in PAGES:
            slug = os.path.basename(page)[:-5]
            url = LIVE_ORIGIN + ("/" if slug == "index" else "/" + slug)
            status = head(url)
            if not (isinstance(status, int) and status < 400):
                problems.append(f"LIVE {url} -> {status}")

    total = len(checked_remote)
    if problems:
        print(f"{len(problems)} problem(s) found ({total} external URLs checked):\n")
        for p in problems:
            print("  ✗", p)
        return 1
    print(f"All links OK — {len(PAGES)} pages, {total} external URLs checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
