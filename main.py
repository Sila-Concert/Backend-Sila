from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from routes.user_route import user
from routes.auth_route import get_current_user, authen

# uvicorn main:app --reload

app = FastAPI()

allow_all = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all
)

app.include_router(user, prefix="/user", tags=["User"])
app.include_router(authen, prefix="/auth", tags=["Auth"])

@app.get("/public")
async def public():
    return {"message": "Hello from Public endpoint!"}

@app.get("/private")
async def private(current_user=Depends(get_current_user)):
    return {"message": f"Hello from Private endpoint, {current_user['email']}!"}



