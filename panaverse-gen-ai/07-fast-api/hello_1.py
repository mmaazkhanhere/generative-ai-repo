from fastapi import FastAPI

app: FastAPI = FastAPI() #object of FastAPI class

@app.get('/') 
def index()->dict: 
    return {'message': 'Hello World', 'age': 25}

if __name__ == '__main__': #when the file is run first, name value is equal to main
    import uvicorn
    uvicorn.run("hello_1:app", reload=True) 