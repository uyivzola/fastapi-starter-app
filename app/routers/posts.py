from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router=APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# Read post
# Defining a GET route at the /posts URL that returns a list of Post objects in JSON format.
# The response_model parameter specifies the model that should be used to validate the response.<--
# The db parameter uses the get_db dependency to provide a database session to the route function. --->
# The db.query(models.Post).all() line fetches all Post objects from the database using the provided session. user <---- server
@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return posts


# Read 1 post //:id
    """
Defining a GET route at the /posts/{id} URL that returns a single Post object with the given ID in JSON format.
The response_model parameter specifies the model that should be used to validate the response.
The id parameter is an integer that is provided in the URL path.
The db parameter uses the get_db dependency to provide a database session to the route function.
The db.query(models.Post).filter(models.Post.id == str(id)).first() line fetches the Post object with the given ID from the database using the provided session.
If the Post object is not found, an HTTPException with status code 404 is raised.
    """


@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Oops! 😔💔 Looks like the post with ID {id} you're looking for isn't here. 😞🕵️‍♀️🔍😞")
    return post


# CREATE A POST
    """
This is a POST route that creates a new post in the database.
status_code=status.HTTP_201_CREATED specifies the HTTP status code that will be returned to the client if the post is created successfully.
response_model=schemas.Post specifies that the response will be a Post model.
post: schemas.PostCreate specifies that the request body should be a PostCreate model.
db: Session = Depends(get_db) specifies that we will use the get_db function to get a database session for each request.
new_post = models.Post(**post.dict()) creates a new Post object with the data from the PostCreate model.
db.add(new_post) adds the new post to the database session.
db.commit() saves the new post to the database.
db.refresh(new_post) refreshes the post object in the database session to get the database-generated id and created_at values.
return new_post returns the newly created post as the response to the client.
    """


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Update put/patch
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Query for the post with the specified ID
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # If the post does not exist, raise an HTTP exception with a 404 status code

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Oops!😔💔 Looks like the post with ID {id} you're looking for isn't here. 😞🕵️‍♀️🔍😞")

    # post.update(updated_post.dict(), synchronize_session=False)
    """ 
    update value by sending many values not specified like below
    
    """
    post.title = updated_post.title
    post.content = updated_post.content
    post.published = updated_post.published
    db.commit()  # make changes to DB
    db.refresh(post)  # return updated post to user
    return post

# DELETE POST


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # query the database for the post with the given id
    post = db.query(models.Post).filter(models.Post.id == id)

    # if the post doesn't exist, raise an HTTPException with 404 status code and a message
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Oops!😔💔 Looks like the post with ID {id} you're looking for isn't here. 😞🕵️‍♀️🔍😞")

    # delete the post from the database and commit the changes
    post.delete(synchronize_session=False)
    db.commit()

    # return a response with 204 status code and no content
    return Response(status_code=status.HTTP_204_NO_CONTENT)
