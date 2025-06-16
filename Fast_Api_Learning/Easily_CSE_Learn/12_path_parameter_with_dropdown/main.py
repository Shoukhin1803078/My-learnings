from fastapi import FastAPI
from enum import Enum

app=FastAPI()

class ModelName(str,Enum): # str na dileo hobe
    resnet="resnet"
    efficientnet="efficientnet"
    vgg16="vgg16"
    alexnet="alexnet"
    densenet="densenet"
    mobilenet="mobilenet"


@app.get("/model/{model_name}")
def get_model(model_name:ModelName):
    if model_name==ModelName.resnet:
        return{
            "model_name":model_name,
            "message":"You have selected ResNet model"
        }
    elif model_name==ModelName.efficientnet:
        return{
            "model_name":model_name,
            "message":"You have selected EfficientNet model"
        }
    elif model_name==ModelName.vgg16:
        return{
            "model_name":model_name,
            "message":"You have selected VGG16 model"
        }
    elif model_name==ModelName.alexnet:
        return{
            "model_name":model_name,
            "message":"You have selected AlexNet model"
        }
    elif model_name==ModelName.densenet:
        return{
            "model_name":model_name,
            "message":"You have selected DenseNet model"
        }
    elif model_name==ModelName.mobilenet:
        return{
            "model_name":model_name,
            "message":"You have selected MobileNet model"
        }
    else:
        return{
            "model_name":"No model selected",
            "message":"Please select a valid model"
        }