from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os

router = APIRouter()

def read_template(filename: str) -> str:
    """Read HTML template file"""
    template_path = os.path.join('ui', 'templates', filename)
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"<h1>Template {filename} not found</h1>"

@router.get("/", response_class=HTMLResponse)
async def home():
    """Home page"""
    return read_template('index.html')

@router.get("/signup", response_class=HTMLResponse)
async def signup_page():
    """Signup page"""
    return read_template('signup.html')

@router.get("/login", response_class=HTMLResponse)
async def login_page():
    """Login page"""
    return read_template('login.html')