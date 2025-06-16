from fastapi import FastAPI
from  enum import Enum

app=FastAPI(titel="FastAPI Enum Example")
class Fruit(Enum):
    apple = "apple"
    banana = "banana"
    cherry = "cherry"

@app.get("/fruit/{fruit}")
async def get_fruit(fruit: Fruit):
    return {"fruit": fruit}
    # return {"fruit": fruit.value}

