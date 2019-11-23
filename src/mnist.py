import train
import predict
import buildnn
import PIL 
import numpy as np
import json

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
    with open('./json_test/test3.json') as f:
        data = json.load(f)
    status, cnn_or_err = buildnn.cnn(data)
    if(status):
        cnn = cnn_or_err
        dataresource = train.DataSource()
        trainApp = train.Train(dataresource)
        trainApp.train(cnn)
        print("ok")
    else:
        err = cnn_or_err
        print(err)