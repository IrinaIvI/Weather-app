from fastapi import HTTPException
from schemas import UserSchemeResponse, UserSchemeRequest
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from sqlalchemy.future import select


async def api_registration(
    request_body: UserSchemeRequest, db: AsyncSession
) -> UserSchemeResponse:
    query = await db.execute(select(User).filter(User.name == request_body.name))
    user = query.scalars().first()
    if user:
        raise HTTPException(
            status_code=400, detail="Данный пользователь уже зарегистрирован"
        )

    new_user = User(name=request_body.name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserSchemeResponse(id=new_user.id)


async def exist_user(user_id: int, db: AsyncSession) -> User:
    query = await db.execute(select(User).filter(User.id == user_id))
    user = query.scalars().first()
    if not user:
        raise HTTPException(
            status_code=400, detail="Данный пользователь не зарегистрирован"
        )

    return user
