#!/usr/bin/env python3
"""CLI tool for shortening URLs from the terminal."""

import argparse
import json
import sys
import urllib.request
import urllib.error

DEFAULT_SERVER = "http://localhost:5000"


def shorten(server: str, url: str) -> dict:
    req = urllib.request.Request(
        f"{server}/shorten",
        data=json.dumps({"url": url}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = json.loads(e.read())
        print(f"Error: {body.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        print(f"Is the server running at {server}?", file=sys.stderr)
        sys.exit(1)


def lookup(server: str, code: str) -> dict:
    try:
        req = urllib.request.Request(f"{server}/stats/{code}")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = json.loads(e.read())
        print(f"Error: {body.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="URL Shortener CLI")
    parser.add_argument("--server", default=DEFAULT_SERVER, help=f"Server URL (default: {DEFAULT_SERVER})")
    sub = parser.add_subparsers(dest="command", required=True)

    p_shorten = sub.add_parser("shorten", help="Shorten a URL")
    p_shorten.add_argument("url", help="URL to shorten")
    p_shorten.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")

    p_lookup = sub.add_parser("lookup", help="Look up a short code")
    p_lookup.add_argument("code", help="Short code to look up")
    p_lookup.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")

    args = parser.parse_args()

    if args.command == "shorten":
        result = shorten(args.server, args.url)
        if args.as_json:
            print(json.dumps(result, indent=2))
        else:
            print(f"{result['short_url']}")

    elif args.command == "lookup":
        result = lookup(args.server, args.code)
        if args.as_json:
            print(json.dumps(result, indent=2))
        else:
            print(f"{result['original_url']}")


if __name__ == "__main__":
    main()
