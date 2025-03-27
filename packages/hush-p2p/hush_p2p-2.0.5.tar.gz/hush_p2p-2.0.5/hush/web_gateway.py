from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os
import json
import subprocess
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

def load_password(username: str):
    hush_dir = os.path.expanduser("~/.hush")
    auth_path = os.path.join(hush_dir, f"{username}_auth.json")
    if os.path.exists(auth_path):
        with open(auth_path, "r") as f:
            data = json.load(f)
            return data.get("password")
    return None

def get_known_peers(username: str):
    hush_dir = os.path.expanduser("~/.hush")
    known_path = os.path.join(hush_dir, f"{username}_known_keys.json")
    if os.path.exists(known_path):
        with open(known_path, "r") as f:
            return json.load(f)
    return {}

def get_messages(username: str):
    log_path = os.path.expanduser(f"~/.hush/logs/{username}_messages.log")
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            return f.read()
    return "No messages yet."

def get_port(username: str):
    # You can expand this if you're storing port somewhere else
    return os.getenv("HUSH_PORT", "5001")

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = os.getenv("DASH_USER", "CLI")
    expected_password = load_password(username)

    is_username_valid = secrets.compare_digest(credentials.username, "admin")
    is_password_valid = expected_password and secrets.compare_digest(credentials.password, expected_password)

    if not (is_username_valid and is_password_valid):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return username

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, user: str = Depends(get_current_user)):
    aliases = get_known_peers(user)
    messages = get_messages(user)
    port = get_port(user)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": user,
        "port": port,
        "aliases": aliases,
        "messages": messages
    })



from fastapi import Form  # Make sure this is imported at the top

@app.post("/send")
def send_message(
    target: str = Form(...),
    message: str = Form(...),
    user: str = Depends(get_current_user)
):
    try:
        subprocess.run(
            ["hush", "--username", user, "--port", "5001", "msg", "--target", target, "--message", message],
            check=True
        )
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Message failed to send")

    return RedirectResponse("/", status_code=303)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8787)
