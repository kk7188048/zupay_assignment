from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from typing import List
import pymongo
from bson import ObjectId  
from app.models import Blog, User, DeleteBlogRequest
from app.token import get_current_user, create_access_token, pwd_context
from app.database import blogs_collection
from datetime import datetime, timedelta


router = APIRouter()


@router.post("/blogs")
async def create_blog(blog: Blog, current_user: User = Depends(get_current_user)):
    try:
        existing_blog = blogs_collection.find_one({"title": blog.title})
        if existing_blog:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A blog with the same title already exists. Please choose a different title.")

        if blog.author != current_user.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author name does not match the logged-in user's username")

        # Insert the blog data into the collection
        blog_data = blog.dict()
        blogs_collection.insert_one(blog_data)
        return {"message": "Blog created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@router.get("/blogs", response_model=List[Blog])
async def retrieve_blogs(current_user: User = Depends(get_current_user)):
    try:
        blogs = blogs_collection.find({"author": current_user.username})
        return list(blogs)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@router.get("/blogs/{blog_id}", response_model=Blog)
async def retrieve_blog(blog_id: str, current_user: User = Depends(get_current_user)):
  try:
    blog = blogs_collection.find_one({"_id": ObjectId(blog_id)})
    if not blog:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    if blog["author"] != current_user.username:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to access this blog")

    return blog
  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/blogs")
async def update_blog(blog: Blog, current_user: User = Depends(get_current_user)):
    try:
        existing_blog = blogs_collection.find_one({"author": current_user.username})
        if not existing_blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

        title_updated = False
        content_updated = False

        if blog.title and blog.title != existing_blog["title"]:
            existing_title = blogs_collection.find_one({"title": blog.title})
            if existing_title:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A blog with the updated title already exists. Please choose a different title.")
            existing_blog["title"] = blog.title
            title_updated = True
        
        if blog.content and blog.content != existing_blog["content"]:
            existing_blog["content"] = blog.content
            content_updated = True

        if title_updated or content_updated:
            blogs_collection.update_one({"_id": existing_blog["_id"]}, {"$set": {"title": existing_blog["title"], "content": existing_blog["content"]}})
            response_message = ""
            if title_updated and content_updated:
                response_message = "Title and content updated successfully"
            elif title_updated:
                response_message = "Title updated successfully"
            elif content_updated:
                response_message = "Content updated successfully"
            return {"message": response_message}
        else:
            return {"message": "No updates provided. Blog content remains unchanged."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/blogs")
async def delete_blog(delete_request: DeleteBlogRequest, current_user: User = Depends(get_current_user)):
  try:
    title = delete_request.title

    # Find the blog by title and author (logged-in user)
    blog = blogs_collection.find_one({
        "title": title,
        "author": current_user.username
    })

    if not blog:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    if blog["author"] != current_user.username:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to delete this blog")
    print("message deleted")  
    blogs_collection.delete_one({"_id": blog["_id"]})

    return {"message": "Blog deleted successfully"}

  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/blogs", response_model=List[Blog])
async def retrieve_all_blogs():
    try:
        blogs = blogs_collection.find({})
        return list(blogs)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/blogs/tags/{tag}", response_model=List[Blog])
async def retrieve_blogs_by_tag(tag: str, current_user: User = Depends(get_current_user)):
    try:
        blogs = blogs_collection.find({"tags": tag, "author": current_user.username})
        return list(blogs)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


