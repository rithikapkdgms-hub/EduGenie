from ai_service import ai_mode, generate, offline_answer


async def summarize_text(text: str) -> str:
    prompt = ("Summarize the provided educational text in clear, concise language. Preserve the central facts, "
              "definitions, and any important caveats. Use a short paragraph and bullets when useful.\n\nText:\n" + text)
    try:
        return await generate(prompt)
    except RuntimeError as exc:
        if "not configured" not in str(exc):
            raise
        return offline_answer("summary", text)
