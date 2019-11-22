import train
import predict

nnParameter = [
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
        "name":"conv",
        "sizeX":3,
        "sizeY":3,
        "strideX":2,
        "strideY":2,
        "channel":64
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
        "num":64
    }
    ,
    {
        "name":"act",
        "act_name":"relu"
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
    cnn = trainApp.train(cnn)
    predictApp = predict.Predict()
    predictApp.predict_with_load("./pict/pict.png")