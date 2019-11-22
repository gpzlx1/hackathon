import tensorflow as tf
from PIL import Image
import numpy as np

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

def predict_with_load(image_path):
    model = tf.keras.models.load_model('./model/mnist.h5')
    x = read_image_preprocess(image_path)
    y = model.predict(x)
    ret = {}
    for i in range(10):
        ret[str(i)] = str(y[0][i])
    return ret



