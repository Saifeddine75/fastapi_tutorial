from fastapi import FastAPI

app = FastAPI()

# GET HTTP Request
@app.get("/")

def root():
    return {"Hello": "Mundo"}