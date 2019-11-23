import train
import predict
import PIL 
import numpy as np

nnParameter = [
    {
        "name":"conv",
        "sizeX":3,
        "sizeY":3,
        "strideX":2,
        "strideY":2,
        "channel":16
    }
    ,
    {
        "name":"act",
        "act_name":"relu"
    }
    ,
    {
        "name":"conv",
        "sizeX":3,
        "sizeY":3,
        "strideX":2,
        "strideY":2,
        "channel":32
    }
    ,
    {
        "name":"act",
        "act_name":"relu"
    }
    ,
    {
        "name":"pool",
        "sizeX":2,
        "sizeY":2,
        "strideX":2,
        "strideY":2,
    }
    ,
    {
        "name":"dense",
        "num":120
    }
    ,
    {
        "name":"dense",
        "num":10
    }
]


if __name__ == "__main__":
    cnn = train.CNN(nnParameter)
    dataresource = train.DataSource()
    trainApp = train.Train(dataresource)
    trainApp.train(cnn)
    ret = predict.predict_with_load("./pict/pre.jpg")
    print(ret)