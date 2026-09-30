from ai_service import ai_mode, generate, offline_answer


async def get_learning_recommendations(topic: str, level: str = "Beginner") -> str:
    prompt = ("Create a practical, personalized learning path for the topic below. Organize it from foundations "
              "to advanced work, include a suggested timeline, exercises or a small project, and types of trustworthy "
              "learning resources to seek. Do not invent specific URLs. Adapt to the learner's stated level.\n\n"
              f"Topic: {topic}\nLearner level: {level}")
    try:
        return await generate(prompt)
    except RuntimeError as exc:
        if "not configured" not in str(exc):
            raise
        return offline_answer("path", topic, level)
