from ai_service import ai_mode, generate, offline_answer


async def explain_concept(concept: str) -> str:
    prompt = ("Explain the following concept to a beginner using plain language. Include a short definition, "
              "one helpful analogy or example, and a brief recap.\n\nConcept: " + concept)
    try:
        return await generate(prompt)
    except RuntimeError as exc:
        if "not configured" not in str(exc):
            raise
        return offline_answer("explain", concept)
