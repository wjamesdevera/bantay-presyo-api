from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"API Name": "Bantay Presyo API"}
