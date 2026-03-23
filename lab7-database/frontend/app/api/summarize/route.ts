import { NextResponse } from "next/server";

import { summarizeViaBackend } from "@/lib/summarizeBackend";

/**
 * Lab 7 contract (agents.md):
 * - Browser calls POST /api/summarize only (not FastAPI directly).
 * - useCompletion sends JSON: { prompt, ...extra body fields }.
 * - We forward { text: prompt, max_length } to FastAPI and return plain-text summary.
 */
export async function POST(req: Request) {
  const body = (await req.json().catch(() => ({}))) as Record<string, unknown>;

  const prompt = typeof body.prompt === "string" ? body.prompt : "";
  const maxLengthRaw = body.max_length;
  const maxLength =
    typeof maxLengthRaw === "number" &&
    Number.isFinite(maxLengthRaw) &&
    maxLengthRaw > 0
      ? Math.min(Math.floor(maxLengthRaw), 500)
      : 100;

  const BACKEND_BASE_URL =
    process.env.BACKEND_BASE_URL ?? "http://127.0.0.1:8000";
  const DEV_JWT_TOKEN = process.env.DEV_JWT_TOKEN ?? "dev-token";

  const result = await summarizeViaBackend({
    text: prompt,
    maxLength,
    backendBaseUrl: BACKEND_BASE_URL,
    devJwtToken: DEV_JWT_TOKEN,
  });

  if (!result.ok) {
    return new NextResponse(result.message, { status: result.status });
  }

  return new NextResponse(result.summary, {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}
