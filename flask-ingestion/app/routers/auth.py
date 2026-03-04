from fastapi import Depends, status, APIRouter, HTTPException

router = APIRouter()

@router.get('/test')
def say_test():
    return {"message": "Hello World"}