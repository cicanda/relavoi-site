#!/usr/bin/env python3
"""Verify the industry dropdown on contact.html matches the API's own list.

    python3 check-industries.py
    python3 check-industries.py --api https://api.relavoi.com/v1

The contact form's `<select name="industry">` is the only copy of the industry
list outside relavoi-backend/src/services/reference-data.ts, which is what the
API validates a workspace's `industry` against and what both dashboards build
their dropdown from. This site is static with no build step and makes no API
calls, so nothing but a check binds the two: add a vertical in the backend and
this form would quietly keep offering the old six.

It compares labels, in order, against `GET /v1/reference`. Order matters
because both lists are rendered in the order they are written.

Scheduled, not run on push. It reads a live server, so the API being down for a
minute would otherwise redden a pull request that did not touch this file. A
failure here means the published form and the API disagree, which is a real
failure; it just is not a reason to block a merge. Same split as the external
half of check-links.py. See .github/workflows/industries.yml.

Exits 0 when they match, 1 when they do not, and 2 when the list could not be
fetched, so a network problem is distinguishable from a real mismatch.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CONTACT = os.path.join(HERE, "contact.html")
DEFAULT_API = "https://api.relavoi.com/v1"
TIMEOUT = 20


def labels_in_form(path):
    """The option labels of the industry select, in document order."""
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    select = re.search(
        r'<select[^>]*name="industry"[^>]*>(.*?)</select>', html, re.S
    )
    if not select:
        print(f"FAIL  {os.path.basename(path)} has no <select name=\"industry\">")
        print("      If the field was renamed or removed, update this check with it.")
        sys.exit(1)
    return [m.strip() for m in re.findall(r"<option[^>]*>([^<]*)</option>", select.group(1))]


def labels_from_api(api):
    url = f"{api.rstrip('/')}/reference"
    req = urllib.request.Request(url, headers={"User-Agent": "relavoi-site-check"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
            if res.status != 200:
                print(f"FAIL  {url} answered HTTP {res.status}")
                sys.exit(2)
            payload = json.loads(res.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as err:
        print(f"FAIL  could not reach {url}: {err}")
        print("      This check reads a live server. If the API is down, that is")
        print("      what this means, not that the form is wrong.")
        sys.exit(2)
    except json.JSONDecodeError as err:
        print(f"FAIL  {url} did not answer with JSON: {err}")
        sys.exit(2)

    industries = payload.get("industries")
    if not isinstance(industries, list) or not industries:
        print(f"FAIL  {url} returned no industries")
        sys.exit(2)
    try:
        return [i["label"] for i in industries]
    except (KeyError, TypeError):
        print(f"FAIL  {url} returned industries without a label")
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api", default=os.environ.get("RELAVOI_API", DEFAULT_API))
    args = parser.parse_args()

    form = labels_in_form(CONTACT)
    api = labels_from_api(args.api)

    if form == api:
        print(f"OK    contact.html offers the {len(api)} industries the API accepts, in order.")
        return 0

    print("FAIL  the contact form and the API disagree about the industry list.")
    print(f"      form: {form}")
    print(f"      api:  {api}")
    missing = [label for label in api if label not in form]
    extra = [label for label in form if label not in api]
    if missing:
        print(f"      the form is missing: {missing}")
    if extra:
        print(f"      the form offers what the API does not accept: {extra}")
    if not missing and not extra:
        print("      same labels, different order. Both lists render in written order.")
    print("      Fix contact.html, or the list in")
    print("      relavoi-backend/src/services/reference-data.ts, whichever is behind.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
