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




class Train:
    def __init__(self, DataSource):
        self.data = DataSource

    def train(self, cnn):
        sgd =  tf.keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="./log", histogram_freq=1)
        cnn.model.compile(optimizer=sgd,
                               loss='sparse_categorical_crossentropy',
                               metrics=['accuracy'])
        cnn.model.fit(self.data.train_images, self.data.train_labels,  verbose=1 ,epochs=8, batch_size=500,\
                     validation_data=(self.data.test_images, self.data.test_labels), workers=4, \
                        callbacks=[tensorboard_callback] )
        cnn.model.save("./model/mnist.h5")
        return cnn

