from flask import jsonify

def create_response(data=None, message="Success", status_code=200, **kwargs):
    """
    Standardized response format for Flask.
    Includes success status, message, data, and any extra fields like pagination.
    """
    success = status_code < 400
    
    response = {
        "success": success,
        "message": message,
    }
    
    if data is not None:
        response["data"] = data
        
    # Merge additional fields (like total, page, limit) directly if provided
    # or keep them separate if you prefer. 
    # Based on your previous request for a specific pagination format:
    if kwargs:
        response.update(kwargs)
        
    return jsonify(response), status_code
