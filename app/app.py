from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse  # Import HTMLResponse
from fastapi.staticfiles import StaticFiles  # Import StaticFiles
import os  # Import os module

app = FastAPI()
replica_count = 0

# Security setup
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "admin"

    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# API endpoints
@app.get("/replica_count")
def get_replica_count(username: str = Depends(get_current_username)):
    return {"replica_count": replica_count}

@app.post("/increment")
def increment_replica_count(username: str = Depends(get_current_username)):
    global replica_count
    replica_count += 1
    return {"message": "Replica count incremented successfully"}

@app.post("/decrement")
def decrement_replica_count(username: str = Depends(get_current_username)):
    global replica_count
    if replica_count > 0:
        replica_count -= 1
        return {"message": "Replica count decremented successfully"}
    else:
        return {"message": "Cannot decrement below 0"}

# Serve the frontend
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open(os.path.join("static", "index.html"), "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

# Mount static files (optional if you have static assets like CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")
