from history.schemas import CreateHistory, GetHistory
# from db.db import db_session
from my_app.models import History
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class HistoryService:

    def __init__(self, session: Session ):
        self.session = session

    def create_history(self, history: CreateHistory, user_id: int) -> History:
        new_history = History(**history.dict(), user_id=user_id)
        self.session.add(new_history)
        self.session.commit()
        self.session.refresh(new_history)

        return new_history

    def get_user_history(self, user_id: int, offset: int, limit: int):
        user_history = self.session.execute(select(History).where(user_id == user_id).offset(offset).limit(limit))
        if user_history:
            return user_history.scalars().fetchall()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has no history"
        )

    def clear_all_history(self, user_id: int):

        statement = select(History).where(user_id=user_id)
        user_history = self.session.execute(statement)

        self.session.delete(user_history)

        self.session.commit()

        return None

    def clear_one_history(self, history_id: int, user_id: int):

        statement = select(History).where(id=history_id, user_id=user_id)
        result = self.session.execute(statement)

        self.session.delete(result.one())
        self.session.commit()

        return None
