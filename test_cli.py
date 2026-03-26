"""Tests for the CLI tool."""

import json
import subprocess
import sys


def run_cli(*args):
    result = subprocess.run(
        [sys.executable, "cli.py", *args],
        capture_output=True, text=True, timeout=10
    )
    return result


def test_cli_help():
    r = run_cli("--help")
    assert r.returncode == 0
    assert "URL Shortener CLI" in r.stdout


def test_shorten_help():
    r = run_cli("shorten", "--help")
    assert r.returncode == 0
    assert "url" in r.stdout.lower()


def test_lookup_help():
    r = run_cli("lookup", "--help")
    assert r.returncode == 0
    assert "code" in r.stdout.lower()


def test_shorten_no_server():
    r = run_cli("--server", "http://localhost:59999", "shorten", "https://example.com")
    assert r.returncode == 1
    assert "Connection error" in r.stderr or "error" in r.stderr.lower()


def test_no_command():
    r = run_cli()
    assert r.returncode != 0
