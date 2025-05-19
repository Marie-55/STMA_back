from datetime import datetime, date
from sqlalchemy.orm import Query

def format_response(data):
    """
    Format data for JSON response
    
    Args:
        data: Data to format (can be SQLAlchemy model, dict, list, or primitive type)
        
    Returns:
        Formatted data suitable for JSON serialization
    """
    # Handle None
    if data is None:
        return None
        
    # Handle lists/iterables
    if isinstance(data, (list, tuple, set, Query)):
        return [format_response(item) for item in data]
        
    # Handle dictionaries
    if isinstance(data, dict):
        return {
            key: format_response(value) 
            for key, value in data.items()
        }
        
    # Handle dates and datetimes
    if isinstance(data, (datetime, date)):
        return data.isoformat()
        
    # Handle SQLAlchemy models
    if hasattr(data, '__dict__'):
        result = {}
        for key, value in data.__dict__.items():
            # Skip SQLAlchemy internal attributes
            if not key.startswith('_'):
                result[key] = format_response(value)
        return result
        
    # Handle primitive types
    return data