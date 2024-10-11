from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
from app.db.models import User

async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).filter(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()

async def create_user(db: AsyncSession, email: str, username: str, password: str):
    hashed_password = bcrypt.hash(password)
    new_user = User(email=email, username=username, password_hash=hashed_password)
    db.add(new_user)
    try:
        await db.commit()
    except IntegrityError:
        return None
    await db.refresh(new_user)
    return new_user
