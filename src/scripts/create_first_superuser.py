import asyncio
from sqlalchemy import select

from app.core.database import AsyncSession, local_session
from app.core.config import settings
from app.models.user import User
from app.core.security import get_password_hash

async def create_first_user(session: AsyncSession) -> None:
    name = settings.ADMIN_NAME
    email = settings.ADMIN_EMAIL
    username = settings.ADMIN_USERNAME
    hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
    
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    
    if user is None:
        session.add(
            User(
                name=name,
                email=email,
                username=username,
                hashed_password=hashed_password, 
                is_superuser=True
            )
        )
        
        await session.commit()

async def main():
    async with local_session() as session:
        await create_first_user(session)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
