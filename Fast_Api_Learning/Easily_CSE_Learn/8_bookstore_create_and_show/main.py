from fastapi import FastAPI
app=FastAPI()

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to FastAPI Learning!"
    }

@app.get("/book_id/{book_id}")
async def read_root(book_id:int):
    return {
        "Book_ID":f"your book id is :{book_id}",
        "title":"FastAPI Learning",
        "author":"Alamin",
    }
