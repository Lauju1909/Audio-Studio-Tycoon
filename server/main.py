import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Audio Studio Tycoon Mod API")

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-anon-key")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Datenmodelle
class User(BaseModel):
    username: str
    password: str

class Mod(BaseModel):
    id: str
    name: str
    author: str
    version: str
    description: str
    download_url: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "Audio Studio Tycoon v3.0 API"}

@app.post("/auth/login")
def login(user: User):
    try:
        # Use email-based login for Supabase auth. Here we assume username represents an email for Supabase.
        # Alternatively, you can use username if your Supabase schema is set up perfectly for it.
        # We will map "username" directly to email login here to be simple.
        response = supabase.auth.sign_in_with_password({
            "email": user.username,
            "password": user.password
        })
        return {"access_token": response.session.access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid credentials: {str(e)}")

@app.get("/mods", response_model=List[Mod])
def list_mods():
    try:
        # Fetching all verified mods from Supabase
        response = supabase.table("mods").select("*").eq("is_verified", True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
