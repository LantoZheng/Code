#!/usr/bin/env python3
"""Minimal Wolfram|Alpha MCP server built with FastMCP.

This server exposes a single tool, ``query_wolfram``, which forwards natural
language prompts to the Wolfram|Alpha v2 HTTP API and formats the textual pods
returned by the service. Set the ``WOLFRAM_API_KEY`` environment variable with
your Wolfram|Alpha AppID before launching the server.
"""

from __future__ import annotations

import asyncio
import os
from typing import Coroutine, List, cast

import httpx
from fastmcp import FastMCP

API_ENDPOINT = "https://api.wolframalpha.com/v2/query"
DEFAULT_TIMEOUT = 30.0

mcp = FastMCP("WolframAlphaServer")


class WolframAlphaError(RuntimeError):
    """Base error for Wolfram|Alpha interaction issues."""


async def _fetch_wolframalpha(query: str, app_id: str) -> dict:
    """Call the Wolfram|Alpha HTTP API and return the parsed JSON payload."""
    params = {
        "input": query,
        "appid": app_id,
        "output": "JSON",
        "format": "plaintext",
        "reinterpret": "true",
    }
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        response = await client.get(API_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()

    result = data.get("queryresult")
    if not result:
        raise WolframAlphaError("Unexpected response from Wolfram|Alpha.")
    if not result.get("success", False):
        tips: List[str] = []
        for suggestion in result.get("didyoumeans", []) or []:
            tip = suggestion.get("val")
            if tip:
                tips.append(tip)
        message = result.get("error", {}).get("msg") or result.get("tips")
        detail = f" Suggestions: {', '.join(tips)}" if tips else ""
        raise WolframAlphaError(
            (message or "Wolfram|Alpha could not interpret the input.") + detail
        )

    return result


def _extract_plaintext_sections(result: dict) -> List[str]:
    sections: List[str] = []
    for pod in result.get("pods", []) or []:
        subpods = pod.get("subpods", []) or []
        pod_lines: List[str] = []
        for subpod in subpods:
            text = (subpod.get("plaintext") or "").strip()
            if text:
                pod_lines.append(text)
        if not pod_lines:
            continue
        title = pod.get("title")
        if title:
            sections.append(f"### {title}\n" + "\n".join(pod_lines))
        else:
            sections.append("\n".join(pod_lines))
    return sections


@mcp.tool(name="query_wolfram", description="Query the Wolfram|Alpha API.")
async def query_wolfram(query: str) -> str:
    """Return a formatted textual summary for the given Wolfram|Alpha query."""
    app_id = os.getenv("WOLFRAM_API_KEY")
    if not app_id:
        raise WolframAlphaError(
            "WOLFRAM_API_KEY environment variable is not set; "
            "please export your Wolfram|Alpha AppID before starting the server."
        )

    result = await _fetch_wolframalpha(query, app_id)
    sections = _extract_plaintext_sections(result)
    if not sections:
        return "Wolfram|Alpha returned no textual results for this query."
    return "\n\n".join(sections)


if __name__ == "__main__":
    asyncio.run(cast(Coroutine[object, object, None], mcp.run()))
