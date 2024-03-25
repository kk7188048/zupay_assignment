from fastapi import Depends, HTTPException, status, APIRouter, BackgroundTasks
from app.models import User, Login, UpdateProfileData, TagUpdate
from app.token import get_current_user, create_access_token, pwd_context
from app.database import users_collection
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta


def send_email(email: str, subject: str, message: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "krishnakumar329865@gmail.com"
    sender_password = "xutvhceedwdqwdzk"
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)


async def background_task(email: str, subject: str, message: str):
    send_email(email, subject, message)


router = APIRouter()


@router.post("/register")
async def register(user: User):
    try:
        print(user)
        existing_user = users_collection.find_one({"username": user.username})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
        user.password = pwd_context.hash(user.password)
        users_collection.insert_one(user.dict())
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/login")
async def login(login_data: Login, background_tasks: BackgroundTasks):
    try:
        user = users_collection.find_one({"username": login_data.username})
        if not user or not pwd_context.verify(login_data.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )
        access_token = create_access_token(data={"sub": user["username"]})
        print("before bg")
        background_tasks.add_task(
            background_task,
            user["email"],
            "Login Successful",
            f"Hello {user['username']}, you have successfully logged in.",
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/profile")
async def update_profile(
    data: UpdateProfileData, user: User = Depends(get_current_user)
):
    try:
        updated_data = {}
        if data.name:
            updated_data["username"] = data.name

        if data.password:
            updated_data["password"] = pwd_context.hash(data.password)

        if not updated_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update",
            )

        users_collection.update_one({"username": user.username}, {"$set": updated_data})
        return {"message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/tags/add")
async def add_tags(tag_update: TagUpdate, user: User = Depends(get_current_user)):
    try:
        # Check if tags to be added are not already present in the user's profile
        user_data = users_collection.find_one({"username": user.username})
        print(user.username)
        if user_data and not any(
            tag in user_data.get("tags", []) for tag in tag_update.tags
        ):
            users_collection.update_one(
                {"username": user.username},
                {"$addToSet": {"tags": {"$each": tag_update.tags}}},
            )
            return {"message": "Tags added successfully"}
        else:
            return {"message": "No new tags to add"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/tags/remove")
async def remove_tags(tag_update: TagUpdate, user: User = Depends(get_current_user)):
    try:
        # Check if tags to be removed are present in the user's profile
        user_data = users_collection.find_one({"username": user.username})
        if user_data and all(
            tag in user_data.get("tags", []) for tag in tag_update.tags
        ):
            users_collection.update_one(
                {"username": user.username}, {"$pullAll": {"tags": tag_update.tags}}
            )
            return {"message": "Tags removed successfully"}
        else:
            return {"message": "No tags to remove"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
