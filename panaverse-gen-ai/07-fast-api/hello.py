from fastapi import FastAPI

app: FastAPI = FastAPI() #object of FastAPI class

@app.get('/') #endpoint url (root folder here) #get request
#we have used @ decorator which whenever the get function is called, the function
#below it will be integrated. So whenever api will be called, the index function 
#will also be called
def index()->dict: #api return format is a dict (json object)
    return {'message': 'Hello World', 'PIAIC':'Student'}