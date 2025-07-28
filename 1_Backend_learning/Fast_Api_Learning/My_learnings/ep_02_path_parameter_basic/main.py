# https://www.youtube.com/@zeqtech
#
# Run this file with:
# - uvicorn app:app --reload



from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Tutorial",
)

@app.get("/items/2")
async def get_item_2(item_id: int):
    return {"message": "Item 2, not dynamic"}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}