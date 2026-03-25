#!/usr/bin/env python3
"""
mcp:// URI resolver — reference implementation of draft-serra-mcp-discovery-uri

Usage:
    python3 resolve.py mcp://example.com
    python3 resolve.py mcp://viti.com/shop
"""

import sys
import json
import urllib.request
import urllib.error
import dns.resolver


def resolve(mcp_uri: str) -> dict | None:
    """Resolve an mcp:// URI to a manifest following the discovery sequence."""

    if not mcp_uri.startswith("mcp://"):
        raise ValueError(f"Not an mcp:// URI: {mcp_uri}")

    rest = mcp_uri[6:]
    host = rest.split("/")[0].split("?")[0]

    # Step 1 — well-known URI
    manifest = _try_well_known(host)
    if manifest:
        return manifest

    # Step 2 — DNS TXT record
    manifest = _try_dns_txt(host)
    if manifest:
        return manifest

    # Step 3 — direct endpoint
    manifest = _try_direct(host)
    if manifest:
        return manifest

    return None


def _try_well_known(host: str) -> dict | None:
    url = f"https://{host}/.well-known/mcp-server"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as r:
            if r.status == 200:
                return json.loads(r.read())
    except Exception:
        pass
    return None


def _try_dns_txt(host: str) -> dict | None:
    try:
        answers = dns.resolver.resolve(f"_mcp.{host}", "TXT")
        for rdata in answers:
            txt = b"".join(rdata.strings).decode()
            if txt.startswith("v=mcp1"):
                fields = dict(f.split("=", 1) for f in txt.split(";") if "=" in f)
                if "endpoint" in fields:
                    return {
                        "mcp_version": "unknown",
                        "name": host,
                        "endpoint": fields["endpoint"].strip(),
                        "transport": "http",
                        "auth": {"type": fields.get("auth", "none").strip()},
                        "_source": "dns_txt",
                    }
    except Exception:
        pass
    return None


def _try_direct(host: str) -> dict | None:
    url = f"https://{host}/mcp"
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps({
                "jsonrpc": "2.0", "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2025-06-18", "capabilities": {}}
            }).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            if r.status == 200:
                return {
                    "mcp_version": "unknown",
                    "name": host,
                    "endpoint": url,
                    "transport": "http",
                    "_source": "direct",
                }
    except Exception:
        pass
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 resolve.py mcp://example.com")
        sys.exit(1)

    uri = sys.argv[1]
    result = resolve(uri)

    if result:
        print(json.dumps(result, indent=2))
    else:
        print(f"No MCP server found for {uri}", file=sys.stderr)
        sys.exit(1)
