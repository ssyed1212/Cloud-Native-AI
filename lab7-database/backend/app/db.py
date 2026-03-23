from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

import datetime


def _engine(database_url: str) -> Engine:
    return create_engine(database_url, pool_pre_ping=True)


def ensure_schema(*, database_url: str) -> None:
    """
    Ensure the summaries table exists and has the expected columns.

    Docker's init SQL only runs on first database initialization; this makes the
    backend resilient when the schema evolves (e.g., adding latency_ms).
    """
    ddl_create = """
    CREATE TABLE IF NOT EXISTS summaries (
      id BIGSERIAL PRIMARY KEY,
      input_text TEXT NOT NULL,
      summary_text TEXT NOT NULL,
      model TEXT NOT NULL,
      prompt_tokens INTEGER,
      completion_tokens INTEGER,
      total_tokens INTEGER,
      latency_ms INTEGER,
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    """
    ddl_index = """
    CREATE INDEX IF NOT EXISTS summaries_created_at_idx ON summaries (created_at DESC);
    """
    ddl_latency = """
    ALTER TABLE summaries
    ADD COLUMN IF NOT EXISTS latency_ms INTEGER;
    """
    eng = _engine(database_url)
    with eng.begin() as conn:
        conn.execute(text(ddl_create))
        conn.execute(text(ddl_latency))
        conn.execute(text(ddl_index))


def insert_summary(
    *,
    database_url: str,
    input_text: str,
    summary_text: str,
    model: str,
    prompt_tokens: Optional[int],
    completion_tokens: Optional[int],
    total_tokens: Optional[int],
    latency_ms: Optional[int],
) -> int:
    sql = """
    INSERT INTO summaries (
      input_text,
      summary_text,
      model,
      prompt_tokens,
      completion_tokens,
      total_tokens,
      latency_ms
    )
    VALUES (
      :input_text,
      :summary_text,
      :model,
      :prompt_tokens,
      :completion_tokens,
      :total_tokens,
      :latency_ms
    )
    RETURNING id
    """
    eng = _engine(database_url)
    with eng.begin() as conn:
        result = conn.execute(
            text(sql),
            {
                "input_text": input_text,
                "summary_text": summary_text,
                "model": model,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "latency_ms": latency_ms,
            },
        )
        row = result.first()
        if not row:
            raise RuntimeError("insert failed: no id returned")
        return int(row[0])


def fetch_recent_summaries(*, database_url: str, limit: int) -> list[dict[str, Any]]:
    sql = """
    SELECT
      id,
      input_text,
      summary_text,
      model,
      prompt_tokens,
      completion_tokens,
      total_tokens,
      latency_ms,
      created_at
    FROM summaries
    ORDER BY created_at DESC, id DESC
    LIMIT :limit
    """
    eng = _engine(database_url)
    with eng.connect() as conn:
        result = conn.execute(text(sql), {"limit": limit})
        cols = list(result.keys())
        rows = []
        for row in result.fetchall():
            rec = dict(zip(cols, row))
            created_at = rec.get("created_at")
            # pydantic v2 won't coerce datetime -> string; normalize to ISO string.
            if isinstance(created_at, datetime.datetime):
                rec["created_at"] = created_at.isoformat()
            rows.append(rec)
        return rows

