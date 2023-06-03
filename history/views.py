from history.schemas import GetHistory
from history.services import HistoryService
# from db.db import db_session
from my_app.models import History
from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession
# import fastapi_users
from sqlalchemy.orm import Session
from typing import List


from my_app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# current_user = fastapi_users.current_user()

router = APIRouter(
    # dependencies= [Depends(current_user)]
)


@router.get("/user/history", response_model=List[GetHistory])
def get_user_history(session: Session = Depends(get_db), offset: int = 0, limit: int = Query(default=20, lte=20)) -> List[History]:
    user_history = HistoryService(session=session)
    user_id = 1
    return  user_history.get_user_history(user_id= user_id, limit=limit, offset=offset)


@router.delete("/remove/all", response_model=GetHistory)
def remove_all_history(session: Session= Depends(get_db) ):
    user_id = 1
    all = HistoryService(session=session)
    return  all.clear_all_history(user_id= user_id)


@router.delete("/remove/{id}", response_model=GetHistory)
def remove_one_item(id: int, session: Session = Depends(get_db) ):
    user_id = 1
    item = HistoryService(session=session).clear_one_history(history_id =id,  user_id=user_id)
    return  item
    

# To create the history, there's no need for an endpoint.
# The function can just be called from the services module directly.

