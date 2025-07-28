# https://www.youtube.com/@zeqtech
#
# In the command line type:
# - pip install -r requirements.txt
#   or
# - pip install fastapi uvicorn

# Run in the command line with:
# - uvicorn app:app --reload

# Visit:
# - http://localhost:8000/docs
#   or
# - http://localhost:8000/redoc


from fastapi import FastAPI

app = FastAPI(
    title="Zeq Tech's FastAPI Tutorial",
    description="## **This is a tutorial**",
    summary="Subscribe!",
    version="1.0.0"
)

# GET Request
@app.get("/")
def index():
    return {"Hello": "World"}

# POST Request
@app.post("/")
def index_post():
    return {"message": "Post request"}

# PUT Request
@app.put("/")
def index_put():
    return {"message": "Put request"}

# DELETE Request
@app.delete("/")
def index_delete():
    return {"message": "Delete request"}