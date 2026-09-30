from ai_service import ai_mode, generate, offline_answer, parse_json


async def generate_quiz(text: str):
    prompt = ("Create exactly three multiple-choice questions from this study material. Each question must have "
              "four options and exactly one correct answer. Return only JSON as an array of objects with keys "
              '"question", "options" (array of four strings), "answer" (exactly matching one option), '
              'and "explanation".\n\nStudy material:\n' + text)
    try:
        result = parse_json(await generate(prompt, json_output=True))
        if not isinstance(result, list) or len(result) != 3:
            raise ValueError("Quiz response must contain exactly three questions")
        for item in result:
            if (not isinstance(item.get("options"), list) or len(item["options"]) != 4
                    or item.get("answer") not in item["options"]):
                raise ValueError("Quiz response has invalid options or answer")
        return result
    except RuntimeError as exc:
        if "not configured" not in str(exc):
            raise
        return offline_answer("quiz", text)
