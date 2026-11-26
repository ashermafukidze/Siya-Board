from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pandas as pd
import requests


class DataSourceError(RuntimeError):
    """Raised when a configured business data source cannot be read."""


def _trim(value: Any, limit: int = 12000) -> str:
    text = json.dumps(value, ensure_ascii=False, indent=2, default=str) if not isinstance(value, str) else value
    return text[:limit] + ("\n...[truncated]" if len(text) > limit else "")


def load_financial_context(path_value: str | None, sheet_name: str | None = None) -> str:
    """Read the configured real Excel workbook and return a bounded text snapshot."""
    if not path_value:
        return "No finance workbook is configured. Steve must say that financial data is unavailable."
    path = Path(path_value).expanduser()
    if not path.is_file():
        raise DataSourceError(f"Finance workbook not found: {path}")
    try:
        workbook = pd.ExcelFile(path)
        selected = sheet_name.strip() if sheet_name and sheet_name.strip() else workbook.sheet_names[0]
        if selected not in workbook.sheet_names:
            raise DataSourceError(f"Sheet '{selected}' not found. Available sheets: {workbook.sheet_names}")
        frame = pd.read_excel(path, sheet_name=selected)
        return (
            f"SOURCE: real Excel workbook {path} | sheet: {selected}\n"
            f"COLUMNS: {list(frame.columns)}\n"
            f"ROWS:\n{frame.head(250).to_string(index=False)}"
        )
    except DataSourceError:
        raise
    except Exception as exc:
        raise DataSourceError(f"Could not read finance workbook: {exc}") from exc


def fetch_json_endpoint(url: str | None, token: str | None, label: str) -> str:
    """Fetch a configured JSON REST endpoint without inventing fallback data."""
    if not url:
        return f"No {label} endpoint is configured. The executive must state that this source is unavailable."
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return f"SOURCE: real {label} endpoint {url}\nDATA:\n{_trim(response.json())}"
    except requests.RequestException as exc:
        raise DataSourceError(f"Could not fetch {label} endpoint: {exc}") from exc
    except ValueError as exc:
        raise DataSourceError(f"{label} endpoint did not return valid JSON: {exc}") from exc


def fetch_search(query: str, url: str | None, token: str | None) -> str:
    """Call an optional search API; return no fabricated results when unconfigured."""
    if not url:
        return "No search endpoint is configured. Do not claim to have searched the web."
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.get(url, params={"q": query}, headers=headers, timeout=20)
        response.raise_for_status()
        return f"SOURCE: real search endpoint {url}\nQUERY: {query}\nRESULTS:\n{_trim(response.json())}"
    except requests.RequestException as exc:
        raise DataSourceError(f"Could not fetch search results: {exc}") from exc
    except ValueError as exc:
        raise DataSourceError(f"Search endpoint did not return valid JSON: {exc}") from exc
