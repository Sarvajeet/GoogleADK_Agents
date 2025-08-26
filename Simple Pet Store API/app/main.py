from fastapi import FastAPI

app = FastAPI()

@app.get("/pets")
def _pets():
    return {"message": "This is the /pets endpoint"}

@app.get("/pets/{petId}")
def _pets_petId():
    return {"message": "This is the /pets/{petId} endpoint"}
