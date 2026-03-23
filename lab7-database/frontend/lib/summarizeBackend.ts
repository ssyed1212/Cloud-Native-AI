/**
 * Server-only: call FastAPI POST /summarize with the dev JWT.
 * Used by Next.js route handlers so the browser never sees the token.
 */

export type SummarizeBackendResult =
  | { ok: true; summary: string }
  | { ok: false; status: number; message: string };

export async function summarizeViaBackend(params: {
  text: string;
  maxLength: number;
  backendBaseUrl: string;
  devJwtToken: string;
}): Promise<SummarizeBackendResult> {
  const { text, maxLength, backendBaseUrl, devJwtToken } = params;

  const backendResp = await fetch(`${backendBaseUrl.replace(/\/$/, "")}/summarize`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${devJwtToken}`,
    },
    body: JSON.stringify({
      text,
      max_length: maxLength,
    }),
  });

  const raw = await backendResp.text();

  if (!backendResp.ok) {
    let message = raw;
    try {
      const j = JSON.parse(raw) as { detail?: unknown };
      if (typeof j.detail === "string") {
        message = j.detail;
      } else if (j.detail != null) {
        message = JSON.stringify(j.detail);
      }
    } catch {
      // keep raw text
    }
    return { ok: false, status: backendResp.status, message };
  }

  try {
    const data = JSON.parse(raw) as { summary?: unknown };
    const summary = typeof data.summary === "string" ? data.summary : "";
    return { ok: true, summary };
  } catch {
    return {
      ok: false,
      status: 502,
      message: "Backend returned invalid JSON",
    };
  }
}
