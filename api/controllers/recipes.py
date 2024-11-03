from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas
from ..models.schemas import Recipe


def create(db: Session, recipes, recipe=None):
    # Create a new instance of the Recipes model with the provided data
    db_recipes = models.Recipe(
        recipe_name=recipe.name,
        description=recipe.description
    )
    # Add the newly created Resource object to the database session
    db.add(db_recipes)
    # Commit the changes to the database
    db.commit()
    # Refresh the Resource object to ensure it reflects the current state in the database
    db.refresh(db_recipes)
    # Return the newly created Resource object
    return db_recipes


def read_all(db: Session):
    return db.query(models.Recipe).all()


def read_one(db: Session, recipe_id):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()


def update(db: Session, recipe_id, recipe):
    # Query the database for the specific recipe to update
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    # Extract the update data from the provided 'recipe' object
    update_data = recipe.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_recipe.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated recipe record
    return db_recipe.first()


def delete(db: Session, recipe_id):
    # Query the database for the specific recipe to delete
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    # Delete the database record without synchronizing the session
    db_recipe.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Recipe(status_code=status.HTTP_204_NO_CONTENT)



