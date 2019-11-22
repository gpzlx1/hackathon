import tensorflow as tf
from PIL import Image
import numpy as np

from train import CNN

'''
python 3.7
tensorflow 2.0.0b0
pillow(PIL) 4.3.0
'''
def read_image_preprocess(imagePath):
    img = Image.open(imagePath).convert('L')
    img = img.resize((28,28))
    flatten_img = np.reshape(img, (28, 28, 1))
    x = np.array([1 - flatten_img], dtype=float)
    return x /255.0

class Predict(object):
    def __init__(self):
        self.name = 'predict'

    def predict(self, cnn,image_path):

        #latest = tf.train.latest_checkpoint('./model')
        # 恢复网络权重
        #cnn.model.load_weights(latest)
        # 以黑白方式读取图片
        x = read_image_preprocess(image_path)
        # API refer: https://keras.io/models/model/
        y = cnn.model.predict(x)

        # 因为x只传入了一张图片，取y[0]即可
        # np.argmax()取得最大值的下标，即代表的数字
        print(image_path)
        print(y[0])
        print(sum(y[0]))
        print('        -> Predict digit', np.argmax(y[0]))
    
    def predict_with_load(self, image_path):
        model = tf.keras.models.load_model('./model/mnist.h5')
        x = read_image_preprocess(image_path)
        y = model.predict(x)
        print(image_path)
        print(y[0])
        print('        -> Predict digit', np.argmax(y[0]))



if __name__ == "__main__":
    cnn = CNN()
    app = Predict()
    #app.predict('./pict/pict.png')
    app.predict(cnn,'./pict/2.png')
