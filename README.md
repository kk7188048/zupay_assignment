# ZuPay Blogging Platform
# Due to My laptop ram issue i was not able to dockerize it
ZuPay is a secure blogging platform built with FastAPI and MongoDB, allowing users to register, create, read, update, and delete their blogs. It also provides features such as tagging, following tags, and retrieving blogs based on tags.

## Features

- **User Authentication**: Users can register and login to access their accounts securely.
- **Token-based Authentication**: Utilizes JWT for token-based authentication.
- **Profile Management**: Users can update their profile information including username and password.
- **Tagging System**: Blogs can be tagged with keywords for easy categorization and search.
- **Blog Management**: CRUD operations for creating, reading, updating, and deleting blogs.
- **Followed Tags**: Users can follow tags to receive relevant blog recommendations.


## Requirements

- Python 3.7+
- MongoDB Atlas (or local MongoDB instance)
- FastAPI
- PyJWT
- Passlib
- Pydantic
- pymongo


## API Endpoints
- POST /register: Register a new user.
- POST /login: Login and obtain an access token.
- PUT /profile: Update user profile information.
- PUT /tags/add: Add tags to the user's profile.
- PUT /tags/remove: Remove tags from the user's profile.
- POST /blogs: Create a new blog.
- GET /blogs: Retrieve all blogs.
- GET /blogs/{blog_id}: Retrieve a specific blog by ID.
- PUT /blogs: Update a blog.
- DELETE /blogs: Delete a blog.
- GET /blogs/tags/{tag}: Retrieve blogs by tag.
- GET /dashboard: Retrieve blogs based on followed tags.

