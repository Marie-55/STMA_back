from sqlalchemy.orm import class_mapper
# just a function to convert the tasks retrieved into a dictionary because the direct function is not working
def model_to_dict(model):
    return {c.key: getattr(model, c.key) 
            for c in class_mapper(model.__class__).columns}


# to handle Firebase objects

from src.utils.db_utils import get_active_db_type
from datetime import datetime

def model_to_dict(model_obj):
    """Convert model objects to dictionaries for JSON serialization"""
    if model_obj is None:
        return None
        
    db_type = get_active_db_type()
    
    # If it's already a dict (Firebase), return it
    if isinstance(model_obj, dict):
        return model_obj
        
    # Handle SQLAlchemy models
    result = {}
    for column in model_obj.__table__.columns:
        value = getattr(model_obj, column.name)
        
        # Handle datetime objects for JSON serialization
        if isinstance(value, datetime):
            value = value.isoformat()
            
        result[column.name] = value
        
    return result