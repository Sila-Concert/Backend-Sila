import uvicorn
import firebase_admin
import pyrebase
import json

from firebase_admin import credentials, auth
from fastapi import FastAPI, Request, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from fastapi import Depends, Header, HTTPException

cred = credentials.Certificate('_service_account_keys.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('firebase_config.json')))

authen = APIRouter()

# signup endpoint
@authen.post("/signup", include_in_schema=False)
async def signup(request: Request):
    req = await request.json()
    email = req['email']
    password = req['password']
    if email is None or password is None:
        return HTTPException(detail={'message': 'Error! Missing Email or Password'}, status_code=400)
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return JSONResponse(content={'message': f'Successfully created user {user.email}'}, status_code=200)    
    except:
        return JSONResponse(content={'message': 'Error Creating User'}, status_code=400)
   

# login endpoint
@authen.post("/login", include_in_schema=False)
async def login(request: Request):
    req_json = await request.json()
    email = req_json['email']
    password = req_json['password']
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return JSONResponse(content={'token': jwt}, status_code=200)
    except:
        return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)
   
#Authorization User
async def get_current_user(request: Request):
    try:
        headers = request.headers
        jwt = headers.get('authorization')
        user = auth.verify_id_token(jwt)
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


