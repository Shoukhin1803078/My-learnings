from fastapi import FastAPI
app=FastAPI()

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to FastAPI Learning!"
    }

@app.get("/item/{item_id}")
async def read_root(item_id:str):
    return {
        "message":item_id
    }
