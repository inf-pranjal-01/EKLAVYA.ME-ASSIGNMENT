# Eklavya Content Generator (ASSIGNMENT)

An agent-based pipeline that generates grade-appropriate educational content, reviews it, and refines it if needed. Built with FastAPI and OpenRouter.

---

## What it does

1. **Generator** takes a grade and topic, returns an explanation + 3 MCQs.
2. **Reviewer** evaluates the output for age appropriateness, correctness, and clarity.
3. If the review fails, the Generator runs once more with the reviewer's feedback embedded.

All three steps are visible in the UI.

---

## Setup

**Requirements:** Python 3.9+

```bash
git clone <repo-url>
pip install fastapi uvicorn python-dotenv requests
```

Create a `.env` file in the root:

```
MISC_API_KEY=your_openrouter_key_here
```

---

## Running

```bash
uvicorn main:app --reload
```

Open `http://localhost:8000` in your browser.

---

## Project structure

```
eklavya/
├── main.py              # FastAPI app, pipeline orchestration
├── generator.py         # Generator agent
├── reviewer.py          # Reviewer agent
├── templates/
│   └── index.html       # UI (designed with AI assistance)
├── .env                 # API key (not committed)
└── .gitignore
```

---

## API

`POST /generate`

```json
{
  "grade": 4,
  "topic": "Types of angles"
}
```

Response:

```json
{
  "grade": 4,
  "topic": "Types of angles",
  "generated": { "explanation": "...", "mcqs": [ ... ] },
  "review":    { "status": "fail", "feedback": [ "..." ] },
  "refined":   { "explanation": "...", "mcqs": [ ... ] },
  "error": null
}
```

`refined` is `null` if the review passed. `error` is `null` on success.

---

## Model

Uses `openai/gpt-4o-mini` via OpenRouter. To swap models, change the `"model"` field in `generator.py` and `reviewer.py`.

---

## Notes

- Refinement is limited to one pass by design.
- Both agents save their last output to `generator_output.json` and `reviewer_output.json` respectively — useful for debugging.
- The frontend (`index.html`) was designed with the help of an AI assistant (Claude) and then adapted to fit the pipeline's output structure.
- No database. No auth. This is a local/demo tool.