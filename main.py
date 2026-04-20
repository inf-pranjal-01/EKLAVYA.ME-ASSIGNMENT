from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import os
 
from generator import generate
from reviewer import review
 


app = FastAPI()





class PipelineRequest(BaseModel):
    grade:int
    topic:str




@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse("templates/index.html")



@app.post("/generate")
def run_pipeline(body:PipelineRequest):

    if not body.topic.strip():
        raise HTTPException(status_code=400,detail="Topic cannot be empty.")

    input_data = {"grade": body.grade, "topic": body.topic.strip()}

    try:
        generated = generate(input_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generator failed: {e}")


    try:
        review_result = review(generated, body.grade)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reviewer failed: {e}")

    payload = {
        "generated": generated,
        "review":    review_result,
        "refined":    None,
    }


    if review_result.get("status") == "fail" and review_result.get("feedback"):
        try:
            refined = generate(
                input_data,
                feedback=review_result["feedback"],
                prev_response=generated,
            )
           
            payload["refined"] = refined

        except Exception as e:

            payload["refinement_error"] = str(e)

    return payload




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)