from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import os
import requests
from bs4 import BeautifulSoup
import re
import time

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    app_name = Column(String, index=True)
    carrier = Column(String)
    sms = Column(Text)
    time = Column(String)
    color = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Origin(Base):
    __tablename__ = "origins"
    
    id = Column(Integer, primary_key=True, index=True)
    app_name = Column(String, unique=True, index=True)
    login_url = Column(String, nullable=True)
    url_checked = Column(DateTime, nullable=True)
    color = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Error creating database tables: {e}")

# Pydantic models
class MessageItem(BaseModel):
    app_name: str
    carrier: str
    sms: str
    time: str
    color: str = None

class ConsoleDataPayload(BaseModel):
    meta: Dict[str, Any]
    data: Dict[str, Any]
    message: str = None

class ConsoleDataResponse(BaseModel):
    meta: dict
    data: dict

# FastAPI app
app = FastAPI(title="Console App API")

# CORS middleware - Allow all origins, no restrictions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Color mapping for app names
color_mapping = {}

def get_color_for_app(app_name):
    """Get a consistent color for an app name"""
    if app_name not in color_mapping:
        # Generate a consistent color based on the app name
        hash_value = hash(app_name) % 360
        color_mapping[app_name] = f"hsl({hash_value}, 70%, 60%)"
    return color_mapping[app_name]

def process_incoming_data(payload: ConsoleDataPayload, db: Session):
    """Process incoming data and store in database"""
    if not payload.data or "messages" not in payload.data:
        return
    
    messages = payload.data["messages"]
    if not messages:
        return
    
    # Clear old messages (keep only latest batch)
    db.query(Message).delete()
    
    # Track unique origins
    unique_origins = set()
    
    # Reverse messages so newest ones are processed last (get latest created_at)
    # This ensures newest messages appear first when ordered by created_at desc
    reversed_messages = list(reversed(messages))
    
    # Process and store each message with incremental timestamps
    base_time = datetime.utcnow()
    for i, msg in enumerate(reversed_messages):
        # Extract app name if not provided
        app_name = msg.get("app_name", "Unknown")
        sms_content = msg.get("sms", "")
        
        # If app_name not in message, try to extract from SMS
        if app_name == "Unknown" and sms_content and ":" in sms_content:
            app_name = sms_content.split(":")[0].strip()
            sms_content = ":".join(sms_content.split(":")[1:]).strip()
        
        # Assign color if not provided
        color = msg.get("color") or get_color_for_app(app_name)
        
        # Add to unique origins
        unique_origins.add((app_name, color))
        
        # Create message record with incremental timestamp
        # Each message gets a slightly later timestamp to ensure proper ordering
        message_time = base_time + timedelta(seconds=i)
        db_message = Message(
            app_name=app_name,
            carrier=msg.get("carrier", ""),
            sms=sms_content,
            time=msg.get("time", ""),
            color=color,
            created_at=message_time
        )
        db.add(db_message)
    
    # Update origins table
    for app_name, color in unique_origins:
        existing_origin = db.query(Origin).filter(Origin.app_name == app_name).first()
        if not existing_origin:
            # Create new origin
            new_origin = Origin(
                app_name=app_name,
                color=color
            )
            db.add(new_origin)
        else:
            # Update color if changed
            existing_origin.color = color
            existing_origin.updated_at = datetime.utcnow()
    
    db.commit()

# Helper function to get messages from database
def get_messages_from_db(db: Session):
    """Retrieve all messages from database"""
    messages = db.query(Message).order_by(Message.created_at.desc()).all()
    return [
        {
            "app_name": msg.app_name,
            "carrier": msg.carrier,
            "sms": msg.sms,
            "time": msg.time,
            "color": msg.color
        }
        for msg in messages
    ]

def find_login_url(app_name: str) -> Optional[str]:
    """Crawl and find login URL for an app"""
    try:
        # Common search patterns
        search_queries = [
            f"{app_name} login",
            f"{app_name} sign in",
            f"{app_name} official website login"
        ]
        
        # Try to find official website
        search_url = f"https://www.google.com/search?q={search_queries[0]}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        
        # Use html.parser instead of lxml for Python 3.13 compatibility
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for login-related links
        login_patterns = [
            r'https?://[^/]*' + re.escape(app_name.lower()) + r'[^/]*/login',
            r'https?://[^/]*' + re.escape(app_name.lower()) + r'[^/]*/signin',
            r'https?://[^/]*' + re.escape(app_name.lower()) + r'[^/]*/auth',
            r'https?://accounts\.' + re.escape(app_name.lower()),
            r'https?://login\.' + re.escape(app_name.lower()),
        ]
        
        # Search in all links
        for link in soup.find_all('a', href=True):
            href = link['href']
            for pattern in login_patterns:
                if re.search(pattern, href, re.IGNORECASE):
                    # Clean up Google redirect URLs
                    if 'google.com/url?q=' in href:
                        href = href.split('google.com/url?q=')[1].split('&')[0]
                    return href
        
        # Fallback: try common patterns
        common_urls = [
            f"https://www.{app_name.lower()}.com/login",
            f"https://{app_name.lower()}.com/login",
            f"https://accounts.{app_name.lower()}.com",
            f"https://login.{app_name.lower()}.com",
        ]
        
        for url in common_urls:
            try:
                test_response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
                if test_response.status_code < 400:
                    return url
            except:
                continue
        
        return None
    except Exception as e:
        print(f"Error finding login URL for {app_name}: {e}")
        return None

def crawl_origin_url(origin_id: int, db: Session):
    """Background task to crawl and update origin URL"""
    origin = db.query(Origin).filter(Origin.id == origin_id).first()
    if not origin:
        return
    
    login_url = find_login_url(origin.app_name)
    origin.login_url = login_url
    origin.url_checked = datetime.utcnow()
    db.commit()
    print(f"Crawled {origin.app_name}: {login_url or 'Not found'}")

# API Endpoints
@app.post("/api/console-data")
async def post_console_data(payload: ConsoleDataPayload, db: Session = Depends(get_db)):
    """
    Receive console data from external source and store in database.
    Payload should match the format: {"meta": {...}, "data": {"messages": [...]}}
    """
    try:
        process_incoming_data(payload, db)
        return {
            "status": "success",
            "message": "Data stored successfully",
            "count": len(payload.data.get("messages", []))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/console-data", response_model=ConsoleDataResponse)
async def get_console_data(db: Session = Depends(get_db)):
    """Get console data from local database"""
    try:
        messages = get_messages_from_db(db)
        
        return {
            "meta": {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat()
            },
            "data": {
                "messages": messages
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/origins")
async def get_origins(db: Session = Depends(get_db)):
    """Get all unique origins"""
    try:
        origins = db.query(Origin).order_by(Origin.app_name).all()
        return {
            "status": "success",
            "origins": [
                {
                    "id": origin.id,
                    "app_name": origin.app_name,
                    "login_url": origin.login_url,
                    "url_checked": origin.url_checked.isoformat() if origin.url_checked else None,
                    "color": origin.color
                }
                for origin in origins
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/origins/check-all")
async def check_all_origins(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Start crawling all origins to find login URLs"""
    try:
        origins = db.query(Origin).all()
        
        for origin in origins:
            # Add background task for each origin
            background_tasks.add_task(crawl_origin_url, origin.id, db)
        
        return {
            "status": "success",
            "message": f"Started crawling {len(origins)} origins",
            "count": len(origins)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files (for frontend)
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
            "get_console_data": "GET /api/console-data",
            "post_console_data": "POST /api/console-data"
        }
    }

# Mount static files directory for other static assets (CSS, JS, images, etc.)
if os.path.exists(static_dir):
    try:
        app.mount("/static", StaticFiles(directory=static_dir), name="static_files")
    except Exception as e:
        print(f"Warning: Could not mount static files: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)