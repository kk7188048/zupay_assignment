from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from typing import Optional, List
from app.database import users_collection, blogs_collection
from app.models import Blog, User
from app.token import get_current_user

router = APIRouter()


@router.get("/dashboard", response_model=List[Blog])
async def retrieve_blogs_by_followed_tags(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    try:
        user_document = users_collection.find_one({"username": current_user.username})
        print(limit)
        if not user_document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        followed_tags = user_document.get("tags", [])
        blogs = blogs_collection.find({"tags": {"$in": followed_tags}})
        relevance_scores = []

        for blog in blogs:
            relevance_score = sum(2 if tag in followed_tags else 1 for tag in blog["tags"])
            relevance_scores.append((blog, relevance_score))
        sorted_blogs = sorted(relevance_scores, key=lambda x: x[1], reverse=True)
        sorted_blogs = [blog[0] for blog in sorted_blogs]

        return sorted_blogs
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

