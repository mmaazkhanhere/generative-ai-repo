from fastapi import FastAPI

app: FastAPI = FastAPI()

@app.get("/notifications/")
def notifications(filter: str):
    return {"message": "filter "+filter}