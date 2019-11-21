import train
import predict

nnParameter = [
    {
        "name":"conv",
        "sizeX":3,
        "sizeY":3,
        "stride":1,
        "channel":32
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
        "stride":1,
        "channel":64
    }
    ,
    {
        "name":"act",
        "act_name":"relu"
    }
    ,
    {
        "name":"dropout",
        "rate":0.5
    }
    ,
    {
        "name":"conv",
        "sizeX":3,
        "sizeY":3,
        "stride":1,
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
        "sizeX":3,
        "sizeY":3,
        "stride":1
    }
    ,
    {
        "name":"dense",
        "num":120
    }
    ,
    {
        "name":"act",
        "act_name":"relu"
    }
    ,
    {
        "name":"dense",
        "num":40
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
    #predictApp = predict.Predict()
    #predictApp.predict(cnn,"./pict/2.png")