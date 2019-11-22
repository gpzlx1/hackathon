import train
import predict

nnParameter = [
    {
        "name":"conv",
        "sizeX":5,
        "sizeY":5,
        "strideX":1,
        "strideY":1,
        "channel":16
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
        "name":"conv",
        "sizeX":5,
        "sizeY":5,
        "strideX":1,
        "strideY":1,
        "channel":16
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
    #cnn = train.CNN(nnParameter)
    #dataresource = train.DataSource()
    #trainApp = train.Train(dataresource)
    #trainApp.train(cnn)
    ret = predict.predict_with_load("./pict/pict.png")
    print(ret)