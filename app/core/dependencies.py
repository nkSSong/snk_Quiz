from fastapi import Header, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.user.domain.models import User

async def get_current_user(
    user_id: int = Header(None, alias="X-User-Id"),
    db: Session = Depends(get_db)
) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        if user_id is None:
            raise HTTPException(status_code=400, detail="X-User-Id header missing")
        raise HTTPException(status_code=401, detail="User not found")
    return user