from fastapi import FastAPI, Body

app = FastAPI()

@app.post('/hi') #post method
def greet(who: str = Body(embed=True)): #embed true is necessary if passing body
    return f"Hello, {who} with post method..."