from fastapi import FastAPI

app: FastAPI = FastAPI()

@app.get('/in/{pname}')
def student_profile(pname:str):
    return {"Student Name: ", pname}

@app.get('/{org}/student/{student_name}')
def complete_profile(org: str, student_name:str):
    return {"Student Name: ": student_name, "Organisation": org }