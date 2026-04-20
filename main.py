import json
import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from generator import generate
from reviewer import review

load_dotenv()

app = FastAPI(title="Eklavya.ME Content Pipeline")


class ContentRequest(BaseModel):
    grade: int
    topic: str


@app.post("/generate")
async def generate_content(req: ContentRequest):
    result = {
        "grade": req.grade,
        "topic": req.topic,
        "generated": None,
        "review": None,
        "refined": None,
        "error": None,
    }

    try:
        # Step 1: Generate
        generated = generate({"grade": req.grade, "topic": req.topic})
        result["generated"] = generated

        # Step 2: Review
        review_result = review(generated, req.grade)
        result["review"] = review_result

        # Step 3: Refine once if review failed
        if review_result["status"] == "fail":
            refined = generate(
                {"grade": req.grade, "topic": req.topic},
                feedback=review_result["feedback"]
            )
            result["refined"] = refined

    except requests.exceptions.Timeout:
        result["error"] = "Request timed out. Please try again."
        raise HTTPException(status_code=504, detail=result["error"])
    except requests.exceptions.HTTPError as e:
        result["error"] = f"API error: {e.response.status_code}"
        raise HTTPException(status_code=502, detail=result["error"])
    except json.JSONDecodeError:
        result["error"] = "Model returned invalid JSON. Please retry."
        raise HTTPException(status_code=422, detail=result["error"])
    except Exception as e:
        result["error"] = str(e)
        raise HTTPException(status_code=500, detail=result["error"])

    return result


@app.get("/")
async def ui():
    return FileResponse("templates/index.html")