from fastapi import FastAPI, Request, HTTPException

# Local imports
from util import prompt_llm

app = FastAPI()


@app.get("/")
async def health_check():
    return {"ping": "pong"}


@app.post("/recommend-anime")
async def recommend_anime(req: Request):
    try:
        data = await req.json()
        prompt = data["prompt"]
        llm_response = prompt_llm(prompt)
        print(llm_response)
        return {"recommendation": llm_response}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
