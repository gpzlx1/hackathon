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
#池化层后面不能接激活
#激活后面不能接激活
#第一层固定为卷积
#最后一层固定为全连接
# 卷积 conv
# 池化 pool
# 全连接 dense
# dropout
# 激活 act
class CNN(object):
    def __init__(self):
        model = models.Sequential()

        model.add(layers.Conv2D(32, (3, 2), activation='relu', input_shape=(28, 28, 1)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))

        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(10, activation='softmax'))

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