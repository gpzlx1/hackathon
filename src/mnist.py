import train
import predict

if __name__ == "__main__":
    cnn = train.CNN()
    dataresource = train.DataSource()
    trainApp = train.Train(dataresource)
    cnn = trainApp.train(cnn)
    predictApp = predict.Predict()
    predictApp.predict(cnn,"./pict/2.png")