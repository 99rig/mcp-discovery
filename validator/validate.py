#!/usr/bin/env python3
"""
/.well-known/mcp-server manifest validator
Reference implementation of draft-serra-mcp-discovery-uri

Usage:
    python3 validate.py https://mcpstandard.dev/.well-known/mcp-server
    python3 validate.py ./mcp-server.json
"""

import sys
import json
import urllib.request

REQUIRED = ["mcp_version", "name", "endpoint", "transport"]
SHOULD = ["description", "auth", "capabilities"]
MAY = ["categories", "languages", "coverage", "contact", "docs", "last_updated", "crawl"]


def validate(manifest: dict) -> list[str]:
    errors = []
    warnings = []

    # MUST fields
    for field in REQUIRED:
        if field not in manifest:
            errors.append(f"MUST: missing required field '{field}'")

    # transport values
    if "transport" in manifest and manifest["transport"] not in ("http", "stdio"):
        errors.append(f"MUST: 'transport' must be 'http' or 'stdio', got '{manifest['transport']}'")

    # endpoint must be https
    if "endpoint" in manifest and not manifest["endpoint"].startswith("https://"):
        warnings.append(f"SHOULD: 'endpoint' should use HTTPS")

    # SHOULD fields
    for field in SHOULD:
        if field not in manifest:
            warnings.append(f"SHOULD: missing recommended field '{field}'")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate.py <url-or-file>")
        sys.exit(1)

    target = sys.argv[1]

    if target.startswith("http"):
        req = urllib.request.Request(target, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as r:
            manifest = json.loads(r.read())
    else:
        with open(target) as f:
            manifest = json.load(f)

    print(f"Validating manifest...")
    print(json.dumps(manifest, indent=2))
    print()

    errors, warnings = validate(manifest)

    if errors:
        print("ERRORS (MUST fix):")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("  ✓ All required fields present")

    if warnings:
        print("WARNINGS (SHOULD fix):")
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
        print("  ✓ All recommended fields present")

    print()
    if not errors:
        print("✓ Manifest is valid")
        sys.exit(0)
    else:
        print("✗ Manifest has errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
