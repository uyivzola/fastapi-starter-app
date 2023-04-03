from typing import List, Optional
from ..oauth2 import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas, database, oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)
# READ ALL POSTS
# response_model  is used to specify the type of data that will be returned by this endpoint
@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(database.get_db),
              current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 10, search: Optional[str] = ""):
    # Get all posts from the database
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all() # getting only user's id not whole people
    # Return the list of posts
    return posts

# GET SPECIFIC POST by ID
# response_model argument specifies that the response should be serialized according to the Post schema defined in schemas.py
@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int,
             db: Session = Depends(database.get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id ==
                                        id).first()  # Query the post by its ID
    if not post:  # If the post doesn't exist, raise an HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Oops! 😔💔 Looks like the post with ID {id} you're looking for isn't here. 😞🕵️‍♀️🔍😞")
    return post  # If the post exists, return it

# CREATE A ROUTE
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
        # expects a post object from the request body, validated against the Post model in schemas.py
        post: schemas.PostCreate,
        # get a database session using the get_db dependency from database.py
        db: Session = Depends(database.get_db),
        # get the current authenticated user using the get_current_user dependency from oauth2.py
        current_user: int = Depends(oauth2.get_current_user)
):
    # create a new Post model instance with data from the request
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    # add the new post to the database
    db.add(new_post)
    # commit the transaction to the database
    db.commit()
    # refresh the new_post instance to get its database-generated fields
    db.refresh(new_post)
    # return the newly created post to the client
    return new_post

# UPDATE POSTS
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int,
                updated_post: schemas.PostCreate,
                db: Session = Depends(database.get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # Query for the post with the specified ID
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # If the post does not exist, raise an HTTP exception with a 404 status code
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Oops!😔💔 Looks like the post with ID {id} you're looking for isn't here. 😞🕵️‍♀️🔍😞")
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorised to perform requested action.🕵️‍♀️')
    post_query.update(updated_post.dict(), synchronize_session=False)
    # post.title = updated_post.title
    # post.content = updated_post.content
    # post.published = updated_post.published
    db.commit()  # make changes to DB
    db.refresh(post)  # return updated post to user
    return post

# DELETE POST

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(database.get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # query the database for the post with the given id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # if the post doesn't exist, raise an HTTPException with 404 status code and a message
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Oops!😔💔 Looks like the post with ID {id} you're looking for isn't here. 😞🕵️‍♀️🔍😞")
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorised to perform requested action 🕵️‍♀️')
    # delete the post from the database and commit the changes
    post_query.delete(synchronize_session=False)
    db.commit()

    # return a response with 204 status code and no content
    return Response(status_code=status.HTTP_204_NO_CONTENT)
