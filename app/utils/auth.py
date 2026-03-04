import random
import string
from app.enums.auth import UnitOfTime

def simplify_expiration(type: any, time: int):
    if type == UnitOfTime.SECOND.value:
        result = f"{time} {type}"
        
    elif type == UnitOfTime.MINUTE.value:
        result = f"{time} {type}"
        
    elif type == UnitOfTime.HOUR.value:
        result = f"{time} {type}"
        
    elif type == UnitOfTime.DAY.value:
        result = f"{time} {type}"
        
    if result is not None:
        if time > 1:
            return result
        
        return result[:-1]
    
    
def generate_random_token_string(length: int):
    chars = string.ascii_letters + string.digits
    
    random_string = ''.join(random.choice(chars) for _ in range(length))

    return random_string