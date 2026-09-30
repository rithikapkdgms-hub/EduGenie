from ai_service import ai_mode, generate, offline_answer


async def answer_question(question: str) -> str:
    prompt = ("You are EduGenie, a careful educational tutor. Answer the student's question accurately and "
              "concisely, explain important reasoning in accessible language, and say when uncertain.\n\n"
              f"Student question: {question}")
    try:
        return await generate(prompt)
    except RuntimeError as exc:
        if "not configured" not in str(exc):
            raise
        return offline_answer("qa", question)
