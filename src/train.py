import os
import tensorflow as tf
from tensorflow.keras import datasets, layers, models


class DataSource(object):
    def __init__(self):
        # mnist数据集存储的位置，如何不存在将自动下载
        data_path = './data'
        (train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data(path=data_path)
        # 6万张训练图片，1万张测试图片
        train_images = train_images.reshape((60000, 28, 28, 1))
        test_images = test_images.reshape((10000, 28, 28, 1))
        # 像素值映射到 0 - 1 之间
        train_images, test_images = train_images / 255.0, test_images / 255.0

        self.train_images, self.train_labels = train_images, train_labels
        self.test_images, self.test_labels = test_images, test_labels

#有许多限制
#dropout 后面没有激活
#池化层后面不能接激活
#激活后面不能接激活
#第一层固定为卷积
#最后一层固定为全连接
# 卷积 conv
# 池化 pool
# 全连接 dense
# dropout
# 激活 act
def get_next(nnParameter, index):
    length = len(nnParameter)
    if(index + 1 < length):
        if(nnParameter[index+1]["name"] == "act"):
            return True, nnParameter[index+1]["act_name"]
        else:
            return False, False
    else:
        return False, False

class CNN(object):
    def __init__(self, nnParameter):
        model = models.Sequential()
        #先不搞错误处理
        length = len(nnParameter)
        i = 0
        while i < length:
            layer = nnParameter[i]
            if i == 0 and layer["name"] == "conv": #第一层特殊
                status, act_name = get_next(nnParameter, i)
                if status:
                    model.add(layers.Conv2D(layer["channel"], \
                    (layer["sizeX"], layer["sizeY"]), strides=layer["stride"], activation=act_name, input_shape=(28, 28, 1)))
                    i = i + 1
                else:
                    model.add(layers.Conv2D(layer["channel"], \
                    (layer["sizeX"], layer["sizeY"]), strides=layer["stride"], input_shape=(28, 28, 1)))
            
            elif i != length - 1:#不是最后一层

                if layer["name"] == "conv":
                    status, act_name = get_next(nnParameter, i)
                    if status:
                        model.add(layers.Conv2D(layer["channel"], \
                        (layer["sizeX"], layer["sizeY"]), strides=layer["stride"], activation=act_name))
                        i = i + 1
                    else:
                        model.add(layers.Conv2D(layer["channel"], \
                        (layer["sizeX"], layer["sizeY"]), strides=layer["stride"]))

                elif layer["name"] == "dropout":
                    model.add(layers.Dropout(layer["rate"]))

                elif layer["name"] == "dense":
                    model.add(layers.Flatten())
                    status, act_name = get_next(nnParameter, i)
                    if status:
                        model.add(layers.Dense(layer["num"], activation=act_name))
                        i = i + 1
                    else:
                        model.add(layers.Dense(layer["num"]))
                elif layer["name"] == "pool":
                    model.add(layers.MaxPooling2D((layer["sizeX"], layer["sizeY"]), strides=layer["stride"]))
            
            else: #最后一层
                model.add(layers.Dense(10, activation='softmax'))  

            i = i + 1    

        model.summary()

        self.model = model


class Train:
    def __init__(self, DataSource):
        self.data = DataSource

    def train(self, cnn):
        cnn.model.compile(optimizer='adam',
                               loss='sparse_categorical_crossentropy',
                               metrics=['accuracy'])
        cnn.model.fit(self.data.train_images, self.data.train_labels, verbose=1 ,epochs=1)
        return cnn

if __name__ == "__main__":
    cnn = CNN()
    dataresource = DataSource()
    app = Train(dataresource)
    app.train(cnn)