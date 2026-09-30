# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a responsive study assistant with a FastAPI backend and a plain HTML/CSS/JavaScript frontend. It supports question answering, beginner-friendly explanations, three-question quizzes, summaries, and level-aware learning paths.

The document describes Gemini 1.5 Pro and a local LaMini model. This implementation uses Google's maintained `google-genai` SDK and a configurable Gemini model (default `gemini-3.8-flash`, following the current Google AI developer examples). All five tasks use Gemini when an API key is configured. Without a key, an explicit offline demo mode lets you run and explore the interface; its sample output is not a substitute for a language model. The project does not download a multi-gigabyte local model.

## Requirements

- Python 3.10 or newer
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey) (optional; required for live AI responses)

## Run in VS Code

1. Open this project folder in VS Code.
2. Open **Terminal → New Terminal** and create a virtual environment:

   ```powershell
   py -3 -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use the VS Code Command Palette: **Python: Select Interpreter**, then choose `.venv`, or run `.venv\Scripts\python.exe -m pip` in place of `python -m pip` below.

3. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. To enable Gemini, copy `.env.example` to `.env` and add your key:

   ```env
   GEMINI_API_KEY=your_key_here
   GEMINI_MODEL=gemini-3.8-flash
   ```

   Keep `.env` private; it is excluded from Git. Skip this step to use offline demo mode.

5. Start the app from the project root:

   ```powershell
   python -m uvicorn main:app --reload
   ```

6. Open [http://127.0.0.1:8000](http://127.0.0.1:8000). Stop the server with **Ctrl+C**.

## Try the app

- **Ask a question:** “Why is the sky blue?”
- **Explain a concept:** “The Pythagorean theorem”
- **Make a quiz:** paste a short study passage. Gemini mode produces exactly three MCQs; offline mode provides a sample question.
- **Summarize:** paste a passage or notes.
- **Learning path:** enter a topic and select your level.

## Check the service

With the server running, visit [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health); it should return `{"status":"ok","service":"EduGenie"}`. You can also open the interactive API page at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), expand an endpoint, choose **Try it out**, and submit JSON such as:

```json
{"text":"Why do seasons happen?","level":"Beginner"}
```

Each task is also available as a POST API: `/qa`, `/explain`, `/quiz`, `/summarize`, and `/learn/recommendations`. Requests accept `text` (2–20,000 characters) and optional `level`.

## Project layout

```text
main.py                    FastAPI routes and validation
ai_service.py              Gemini integration and offline fallback
qna.py                     Question-answering prompt
explanation_module.py      Concept explanation prompt
quiz_module.py             MCQ generation and response validation
summary_module.py          Summary prompt
learning_path.py           Personalized learning plan prompt
templates/index.html       Accessible web interface
static/style.css           Responsive styling
static/app.js              API form handling and result rendering
requirements.txt           Python dependencies
.env.example               Gemini configuration template
```

## Troubleshooting

- If `py` is not recognized, install Python 3.10+ and enable its PATH option, then reopen VS Code.
- If activation is blocked, select the virtual environment interpreter in VS Code as described above.
- If the page cannot connect, confirm Uvicorn is still running and use `http://127.0.0.1:8000`.
- If Gemini returns an API error, confirm the key is valid, billing/quota permits the request, and `GEMINI_MODEL` is available to your API key. Restart Uvicorn after changing `.env`.
- The model's output is generated content; check important answers against reliable references.
