from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime, timedelta
import requests
import json
import time
import os

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class TokenCache(Base):
    __tablename__ = "token_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text)
    session = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)
    last_checked = Column(DateTime, default=datetime.utcnow)

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Error creating database tables: {e}")

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    meta: dict
    data: dict
    message: str

class ConsoleData(BaseModel):
    meta: dict
    data: dict

# FastAPI app
app = FastAPI(title="Console App API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Default credentials
DEFAULT_EMAIL = "Aktermamber.00.7@gmail.com"
DEFAULT_PASSWORD = "Bd55555$"

# Token cache (in-memory for 5-second rule)
token_cache = {
    "token": None,
    "session": None,
    "last_updated": None,
    "last_checked": None
}

print(f"Default credentials loaded: {DEFAULT_EMAIL}")

# Color mapping for app names
color_mapping = {}

def get_color_for_app(app_name):
    """Get a consistent color for an app name"""
    if app_name not in color_mapping:
        # Generate a consistent color based on the app name
        hash_value = hash(app_name) % 360
        color_mapping[app_name] = f"hsl({hash_value}, 70%, 60%)"
    return color_mapping[app_name]

def process_sms_data(data):
    """Process SMS data to extract app names and assign colors"""
    if not data or "data" not in data or "messages" not in data["data"]:
        return data
    
    messages = data["data"]["messages"]
    if not messages:
        return data
    
    # Process each message
    for message in messages:
        sms_content = message.get("sms", "")
        if sms_content:
            # Extract app name from SMS content (first word before colon)
            if ":" in sms_content:
                app_name = sms_content.split(":")[0].strip()
                # Remove the app name from the SMS content
                remaining_content = ":".join(sms_content.split(":")[1:]).strip()
                message["app_name"] = app_name
                message["sms"] = remaining_content
                message["color"] = get_color_for_app(app_name)
            else:
                # If no colon, use a default app name
                message["app_name"] = "Unknown"
                message["color"] = get_color_for_app("Unknown")
    
    return data

# Helper functions
def get_cached_token():
    """Get cached token if last update was within 5 seconds"""
    if token_cache["last_updated"] and (datetime.utcnow() - token_cache["last_updated"]).seconds < 5:
        return token_cache["token"]
    return None

def update_token_cache(token, session):
    """Update token cache with new values"""
    token_cache["token"] = token
    token_cache["session"] = session
    token_cache["last_updated"] = datetime.utcnow()
    token_cache["last_checked"] = datetime.utcnow()

def perform_login(email, password):
    """Perform login to get initial token and session"""
    url = "https://2oo9.com/api/v1/mnitnetworkcom/auth/login"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://v2.mnitnetwork.com',
        'referer': 'https://v2.mnitnetwork.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
    }
    data = {
        'email': email,
        'password': password
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()
        
        if response.status_code in [200, 201]:
            # Extract session from response
            session = response_data.get("data", {}).get("user", {}).get("session")
            if session:
                # Update token cache
                update_token_cache(None, session)  # We'll get the actual token in hitauth
                return response_data
            else:
                raise Exception(f"Login succeeded but no session found in response: {response_data}")
        else:
            raise Exception(f"Login failed with status {response.status_code}: {response_data}")
    except Exception as e:
        raise Exception(f"Login error: {str(e)}")

def perform_hitauth():
    """Get refreshed token using hitauth endpoint"""
    # Get session from cache
    session = token_cache.get("session")
    if not session:
        # If no session, perform login first
        login_result = perform_login(DEFAULT_EMAIL, DEFAULT_PASSWORD)
        session = login_result.get("data", {}).get("user", {}).get("session")
        if not session:
            raise Exception("Failed to obtain session after login")
    
    # External API call to hitauth
    url = "https://2oo9.com/api/v1/mnitnetworkcom/auth/hitauth"
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://v2.mnitnetwork.com',
        'referer': 'https://v2.mnitnetwork.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
    }
    data = {
        'mnitnetworkcom_session': session,
        'mnitnetworkcom_url': 'https://v2.mnitnetwork.com/dashboard/getnum'
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()
        
        if response.status_code in [200, 201]:
            # Extract token from response
            token = response_data.get("data", {}).get("token")
            if token:
                # Update token cache
                update_token_cache(token, session)
                return token
            else:
                raise Exception(f"Hitauth succeeded but no token found in response: {response_data}")
        else:
            # If hitauth fails, try to login again
            login_result = perform_login(DEFAULT_EMAIL, DEFAULT_PASSWORD)
            session = login_result.get("data", {}).get("user", {}).get("session")
            if session:
                # Retry hitauth with new session
                data['mnitnetworkcom_session'] = session
                retry_response = requests.post(url, headers=headers, data=data)
                retry_data = retry_response.json()
                if retry_response.status_code in [200, 201]:
                    token = retry_data.get("data", {}).get("token")
                    if token:
                        update_token_cache(token, session)
                        return token
            raise Exception(f"Hitauth failed with status {response.status_code}: {response_data}")
    except Exception as e:
        raise Exception(f"Hitauth error: {str(e)}")

# API Endpoints
@app.post("/api/login", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    """Perform login to get initial token and session"""
    try:
        result = perform_login(login_request.email, login_request.password)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/refresh-token")
async def refresh_token():
    """Get refreshed token using hitauth endpoint"""
    # Check if we have a cached token that's still valid (within 5 seconds)
    cached_token = get_cached_token()
    if cached_token:
        return {"token": cached_token, "from_cache": True}
    
    try:
        token = perform_hitauth()
        return {"token": token, "from_cache": False}
    except Exception as e:
        print(f"Error in refresh_token: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/console-data", response_model=ConsoleData)
async def get_console_data():
    """Get console data using the latest token"""
    try:
        # Check if we have a cached token that's still valid (within 5 seconds)
        cached_token = get_cached_token()
        token = cached_token if cached_token else token_cache.get("token")
        
        # If no token, perform hitauth to get one
        if not token:
            token = perform_hitauth()
        
        # External API call to get console data
        url = "https://2oo9.com/api/v1/mnitnetworkcom/dashboard/getconsole"
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
            'content-type': 'application/json',
            'mhitauth': token,
            'origin': 'https://v2.mnitnetwork.com',
            'referer': 'https://v2.mnitnetwork.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response_data = response.json()
        
        if response.status_code in [200, 201]:
            # Process SMS data to extract app names and assign colors
            processed_data = process_sms_data(response_data)
            return processed_data
        elif response.status_code == 401:
            # Token expired, perform hitauth again
            try:
                token = perform_hitauth()
                # Retry the request with new token
                headers['mhitauth'] = token
                retry_response = requests.get(url, headers=headers)
                retry_data = retry_response.json()
                if retry_response.status_code in [200, 201]:
                    # Process SMS data to extract app names and assign colors
                    processed_data = process_sms_data(retry_data)
                    return processed_data
                else:
                    raise Exception(f"Retry failed with status {retry_response.status_code}: {retry_data}")
            except Exception as e:
                raise Exception(f"Failed to refresh token and retry: {str(e)}")
        else:
            raise Exception(f"Console data request failed with status {response.status_code}: {response_data}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files (for frontend)
<<<<<<< HEAD
# Use absolute path to ensure it works in different environments (local, Render, etc.)
static_dir = os.path.join(os.path.dirname(__file__), "static")

# Root route to serve index.html
@app.get("/")
async def root():
    """Root endpoint - serves index.html"""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        from fastapi.responses import FileResponse
        return FileResponse(index_path, media_type="text/html")
    # Fallback if static files don't exist
    return {
        "message": "Console App API",
        "status": "running",
        "endpoints": {
            "login": "/api/login",
            "refresh_token": "/api/refresh-token",
            "console_data": "/api/console-data"
        }
    }

# Mount static files directory for other static assets (CSS, JS, images, etc.)
if os.path.exists(static_dir):
    try:
        app.mount("/static", StaticFiles(directory=static_dir), name="static_files")
    except Exception as e:
        print(f"Warning: Could not mount static files: {e}")
=======
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
>>>>>>> 2019967b1e5d1aca92029604547cdc9354676815

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)