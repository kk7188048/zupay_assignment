from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi import APIRouter
from app.auth import router as authenticate
from app.blogs import router as blogs
from app.dashboard import router as dash

app = FastAPI()
app.include_router(authenticate, tags=["Authorization"])
app.include_router(blogs,tags=["Blogs"])
app.include_router(dash, tags=["Dashboard"])

