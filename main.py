from fastapi import FastAPI
from routes.user_route import user

# uvicorn main:app --reload

app = FastAPI()

app.include_router(user, prefix="/user", tags=["User"])

@app.get("/")
async def home():
    return {"message": "Hello World"}