# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# async def read_root():
#     return {
#         "message": "Welcome to FastAPI Learning!"
#     }

from fastapi import FastAPI
app= FastAPI(title="FastAPI Introduction",description="A simple FastAPI application to demonstrate basic features.",version="1.0.0")

@app.get("/")
def root():
    return {"hello":"hello world"}