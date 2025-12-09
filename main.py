from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any
import json
import os

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
    
    # Process and store each message
    for msg in messages:
        # Extract app name if not provided
        app_name = msg.get("app_name", "Unknown")
        sms_content = msg.get("sms", "")
        
        # If app_name not in message, try to extract from SMS
        if app_name == "Unknown" and sms_content and ":" in sms_content:
            app_name = sms_content.split(":")[0].strip()
            sms_content = ":".join(sms_content.split(":")[1:]).strip()
        
        # Assign color if not provided
        color = msg.get("color") or get_color_for_app(app_name)
        
        # Create message record
        db_message = Message(
            app_name=app_name,
            carrier=msg.get("carrier", ""),
            sms=sms_content,
            time=msg.get("time", ""),
            color=color
        )
        db.add(db_message)
    
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