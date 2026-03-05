from fastapi.responses import JSONResponse
from app.enums.response_status import ResponseStatus

def create_response(status: ResponseStatus, message: str, data: any = None, status_code: int = 200) -> JSONResponse:
    """Helper function to create a JSONResponse with a standardized format."""
    content = {
        "success": status == ResponseStatus.SUCCESS,
        "message": message,
        "data": data,
    }
    return JSONResponse(status_code=status_code, content=content)
