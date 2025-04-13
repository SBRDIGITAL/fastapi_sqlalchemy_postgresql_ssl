import os, sys
from typing import Optional

from fastapi import FastAPI

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from database.db_connection import DbSession, db_session



class CRUD:
    
    def __init__(self, db_session: DbSession = db_session) -> None:
        """
        ## Инициализирует класс `CRUD` для работы с базой данных.

        Args:
            db_session (DbSession, optional):
                Экземпляр сессии базы данных. По умолчанию используется `db_session`.
        """     
        self.db_session = db_session
        self.AsyncSessionLocal: AsyncSession = self.db_session.AsyncSessionLocal

    async def select_version(self, session: Optional[AsyncSession] = None) -> str:
        """
        ## Возвращает информацию о версии `PostgreSQL`.
        
        Args:
            session (Optional[AsyncSession]): Сессия, в которой выполняются транзакции.
                Если None, создается новая сессия.
        
        Returns:
            str: Информация о версии `PostgreSQL`.
        """
        async with (session or self.AsyncSessionLocal()) as session:
            try:  # Используем переданную сессию или создаем новую
                async with session.begin():
                    res = await session.execute(text("SELECT VERSION()"))
                    version = res.scalar()
                    pv = f'Версия PostgreSQL: {version}'
                    print(pv)
                    return pv
                    
            except Exception as ex:
                await session.rollback()
                raise ex



db_crud = CRUD()
app = FastAPI()



@app.get("/postgres_version")
async def postgres_version():
    """
    ## Эндпоинт для получения информации о версии `PostgreSQL`.

    Returns:
        dict: Словарь, содержащий информацию о версии `PostgreSQL`.
    """    
    msg = await db_crud.select_version()
    print(msg)
    return {"info": msg}