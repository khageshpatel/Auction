from fastapi import HTTPException
from asyncpg.exceptions import ForeignKeyViolationError
from sqlalchemy.exc import IntegrityError

def Handle(ex):
    try:
        raise ex
    except IntegrityError as exception:
        raise HTTPException(status_code=303, detail="DB integrity error for example foreign key")
    except ForeignKeyViolationError as excception:
        raise HTTPException(status_code=303, detail="Foreign key violated")

