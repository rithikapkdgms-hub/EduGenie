"""Shared Gemini client with an intentional, dependency-free offline fallback."""
import json
import os
from functools import lru_cache


def ai_mode() -> str:
    return "gemini" if os.getenv("GEMINI_API_KEY", "").strip() else "offline-demo"


@lru_cache(maxsize=1)
def _client():
    from google import genai

    return genai.Client(api_key=os.environ["GEMINI_API_KEY"])


async def generate(prompt: str, *, json_output: bool = False) -> str:
    """Generate content via the official Google GenAI SDK, otherwise use local fallback."""
    if not os.getenv("GEMINI_API_KEY", "").strip():
        raise RuntimeError("Gemini is not configured")
    from google.genai import types

    config = types.GenerateContentConfig(temperature=0.4, max_output_tokens=1800)
    if json_output:
        config = types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=1800,
            response_mime_type="application/json",
        )
    response = await _client().aio.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
        contents=prompt,
        config=config,
    )
    if not response.text:
        raise RuntimeError("The AI returned an empty response. Please try again.")
    return response.text.strip()


def parse_json(text: str):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text)


def offline_answer(task: str, text: str, level: str = "Beginner"):
    """Simple clearly-labeled fallback, so the project starts without credentials."""
    topic = text.strip().rstrip("?.!")
    if task == "qa":
        return (f"Offline demo answer: I can help explore ‘{topic}’. Add a Gemini API key in .env "
                "for a detailed AI-generated answer. Try asking a focused question, such as “What is photosynthesis?”")
    if task == "explain":
        return (f"{topic.title()} — beginner-friendly overview\n\n"
                f"Think of {topic} as a subject to break into smaller parts. Start by learning its key terms, "
                "then look at a simple example, and finally explain the idea in your own words. "
                "This is an offline sample; configure Gemini for a topic-specific explanation.")
    if task == "summary":
        words = text.split()
        return " ".join(words[: min(45, max(20, len(words) // 3))]) + ("…" if len(words) > 45 else "")
    if task == "quiz":
        return [{"question": f"Which is the best first step when studying {topic}?",
                 "options": ["Learn key terms", "Skip the examples", "Memorize without context", "Avoid practice"],
                 "answer": "Learn key terms", "explanation": "Key terms make later examples easier to understand."}]
    if task == "path":
        return (f"## Learning path: {topic}\n\n**Level:** {level}\n\n"
                "1. **Foundations (Week 1):** Learn core vocabulary and prerequisites.\n"
                "2. **Core ideas (Weeks 2–3):** Study the main concepts and work through guided examples.\n"
                "3. **Practice (Week 4):** Solve exercises and explain your reasoning.\n"
                "4. **Build (Weeks 5–6):** Complete a small project and review gaps.\n\n"
                "Configure Gemini in .env for recommendations tailored to this topic.")
    return "Offline demo mode is active."
