from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    company_name: str = os.getenv("COMPANY_NAME", "Siyabonga Technology")
    ceo_name: str = os.getenv("CEO_NAME", "Asher")
    model: str = os.getenv("LLM_MODEL", "gpt-5.5")
    reasoning_effort: str = os.getenv("LLM_REASONING_EFFORT", "low")
    finance_excel_path: str = os.getenv("FINANCE_EXCEL_PATH", "")
    finance_sheet_name: str = os.getenv("FINANCE_SHEET_NAME", "")
    crm_api_url: str = os.getenv("CRM_API_URL", "")
    crm_api_token: str = os.getenv("CRM_API_TOKEN", "")
    marketing_api_url: str = os.getenv("MARKETING_API_URL", "")
    marketing_api_token: str = os.getenv("MARKETING_API_TOKEN", "")
    search_api_url: str = os.getenv("SEARCH_API_URL", "")
    search_api_token: str = os.getenv("SEARCH_API_TOKEN", "")
    transcript_path: str = os.getenv("TRANSCRIPT_PATH", "logs/boardroom.jsonl")
    max_history_messages: int = int(os.getenv("MAX_HISTORY_MESSAGES", "80"))

    @property
    def transcript_file(self) -> Path:
        path = Path(self.transcript_path).expanduser()
        return path if path.is_absolute() else ROOT / path


def get_settings() -> Settings:
    return Settings()
