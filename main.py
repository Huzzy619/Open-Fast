from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import openai
from decouple import config
from fastapi import Depends, FastAPI, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from my_app import models, schemas, crud
from my_app.database import SessionLocal, engine
from history.views import router as history_router
from typing import List
SQLModel.metadata.create_all(bind=engine)
# models.Base.metadata.create_all(bind=engine)


openai.api_key = config('AI_API_KEY')

app = FastAPI()

app.include_router(router= history_router)

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db : Session = Depends(get_db) ):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0 , limit = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db:Session = Depends(get_db)):
    return crud.create_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db:Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items










app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})








@app.get('/')
async def index():
    # print()
    # json = openai.Completion.create(
    # model="text-davinci-002",
    # prompt="The net worth of the richest footballer",
    # max_tokens=6,
    # temperature=0
    #     )

    # # print(response['detail'])
    # return {
    #     # "detail":"ok",
    #     # "list" : openai.Model.list()
    #     # 'res': response,
    #     "model":json["model"], 
    #     "choice_txt":json["choices"][0]['text']
    # }
    return {
        "hello": "world"
    }

@app.get('/create')
async def index():
    json = openai.Completion.create(
    model="text-davinci-002",
    prompt="The net worth of the richest footballer",
    max_tokens=6,
    temperature=0
        )

    return {
        # "detail":"ok",
        # "list" : openai.Model.list()
        # 'res': response,
        "model":json["model"], 
        "choice_txt":json["choices"][0]['text']
    }

@app.get('/edit')
def correct_spelling():
    response = openai.Edit.create(
    model="text-davinci-edit-001",
    input="I tink i lost my pen?",
    instruction="Fix the spelling mistakes"
    )
    return {
        'response':response
    }

@app.get('/code')
def explain_code():

    string = """
    def updatecart(request):
    if request.method == "POST":
        prod_id = int(request.POST['prod_id'])

        if (Cart.objects.filter(product_id=prod_id, user=request.user)):
            new_product_qty = int(request.POST['product_qty'])

            Cart.objects.filter(product_id=prod_id, user=request.user) \
                .update(product_qty=new_product_qty)

            # cart.product_qty = new_product_qty

            # cart.save()
            # cart.update(product_qty = new_product_qty)

            return JsonResponse({'status': "Cart updated"})

    return redirect('home')
    
    
    """
    response = openai.Completion.create(
    model="code-davinci-002",
    prompt="class Log:\n    def __init__(self, path):\n        dirname = os.path.dirname(path)\n        os.makedirs(dirname, exist_ok=True)\n        f = open(path, \"a+\")\n\n        # Check that the file is newline-terminated\n        size = os.path.getsize(path)\n        if size > 0:\n            f.seek(size - 1)\n            end = f.read(1)\n            if end != \"\\n\":\n                f.write(\"\\n\")\n        self.f = f\n        self.path = path\n\n    def log(self, event):\n        event[\"_event_id\"] = str(uuid.uuid4())\n        json.dump(event, self.f)\n        self.f.write(\"\\n\")\n\n    def state(self):\n        state = {\"complete\": set(), \"last\": None}\n        for line in open(self.path):\n            event = json.loads(line)\n            if event[\"type\"] == \"submit\" and event[\"success\"]:\n                state[\"complete\"].add(event[\"id\"])\n                state[\"last\"] = event\n        return state\n\n\"\"\"\nHere's what the above class is doing:\n1.",
    temperature=0,
    max_tokens=64,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["\"\"\""]
    )
    return {
        "response":response
    }

@app.get('/test')
async def troy():
    json = {
    "id": "cmpl-6A6uhgzi3bkZdumliL9esJ4S7DXcz",
    "object": "text_completion",
    "created": 1667867875,
    "model": "text-davinci-002",
    "choices": [
      {
        "text": "\n\nThis is a test",
        "index": 0,
        "logprobs": None,
        "finish_reason": "length"
      }
    ],
    "usage": {
      "prompt_tokens": 5,
      "completion_tokens": 6,
      "total_tokens": 11
    }
  }
    return{
        "model":json["model"], 
        "choice_txt":json["choices"][0]['text'],
        "completion_tokens": json["usage"]['completion_tokens']

    }
