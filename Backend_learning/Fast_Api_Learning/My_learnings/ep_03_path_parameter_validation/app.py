from fastapi import FastAPI, Path

app = FastAPI()

ITEM_ID_VALIDATION = Path(
    ...,
    title="The String ID of the Item to get",
    max_length=5,
    examples=["abc", "def"],
)

ITEM_AMOUNT_VALIDATION = Path(
    ...,
    title="The number of items to get",
    ge=1,
    le=99
)

@app.get("/items/{item_id}/{amount}")
async def get_item(
    item_id: str = ITEM_ID_VALIDATION,
    amount: int = ITEM_AMOUNT_VALIDATION
):
    return {"item_id": item_id, "amount": amount}