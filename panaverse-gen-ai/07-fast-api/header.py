from fastapi import FastAPI, Header

app: FastAPI = FastAPI()

@app.post('/hi')
def greet(who: str = Header()):
    return f"Hello {who}"