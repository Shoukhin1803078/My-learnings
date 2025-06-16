from fastapi import FastAPI
from enum import Enum
app=FastAPI()

class Model(Enum):
    resnet = "resnet"
    efficientnet = "efficientnet"
    vgg16 = "vgg16"
    alexnet = "alexnet"
    densenet = "densenet"
    mobilenet = "mobilenet"

@app.get("/model/{model_name}")
def model_selection(model_name:Model):
    if model_name == Model.resnet:
        return {
            "model_choosen":model_name,
            "message":"You have selected {model_name} model"
        }
    elif model_name == Model.efficientnet:
        return {
            "model_choosen":model_name,
            "message":"You have selected {model_name} model"
        }
    else:
        return {
            "model_choosen":model_name,
            "message":"You have selected {model_name} model"
        }

@app.get("/")
async def root():
    return {"message": "wel come to fastapi"}


@app.get("/{model_name}")
async def root(model_name:str):
    return {"message": f"you press {model_name} model"}