from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import *
from authentication import (get_hashed_password)

app = FastAPI()

@app.post('/registration')
async def user_registration(user: user_pydanticIn):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_hashed_password(user_info["password"])
    user_obj = User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return{
        "status" : "ok",
        "data" : f"hello {new_user.username}, welcome to this app, check you email."
    }


@app.get('/')
def index():
    return {"Message": "This is test"}


register_tortoise(
    app,
    db_url="sqlite://database.sqllite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)
