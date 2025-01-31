# -*- coding: utf-8 -*-
"""SimpleCnn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wUSuFaNO1PKP-vItgMDVoqWJNsYIxrKU
"""

from google.colab import drive
drive.mount('/content/gdrive')

import zipfile
with zipfile.ZipFile("/content/gdrive/MyDrive/seg_train.zip","r") as zip_ref:
    zip_ref.extractall("targetdir")

import zipfile
with zipfile.ZipFile("/content/gdrive/MyDrive/Test_data.zip","r") as zip_ref:
    zip_ref.extractall("testdir")

import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import PIL
import tensorflow as tf
import pathlib
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

data_dir = pathlib.Path("data")
data_dir = data_dir.joinpath('/content/targetdir/seg_train')
data_dir

image_count = len(list(data_dir.glob('*/*.jpg')))
print(image_count)

buildings = list(data_dir.glob('buildings/*'))
buildings[:5]

PIL.Image.open(str(buildings[1]))

forest = list(data_dir.glob('forest/*'))
PIL.Image.open(str(forest[0]))

Natural_images_dict = {
    'buildings': list(data_dir.glob('buildings/*')),
    'forest': list(data_dir.glob('forest/*')),
    'glacier': list(data_dir.glob('glacier/*')),
    'mountain': list(data_dir.glob('mountain/*')),
    'sea': list(data_dir.glob('sea/*')),
     'street': list(data_dir.glob('street/*')),
}

NatImage_labels_dict = {
    'buildings': 0,
    'forest': 1,
    'glacier': 2,
    'mountain': 3,
    'sea': 4,
    'street': 5,
}

Natural_images_dict['sea'][:5]

str(Natural_images_dict['sea'][0])

img = cv2.imread(str(Natural_images_dict['sea'][0]))

img.shape

cv2.resize(img,(180,180)).shape

X, y = [], []

for NatImg_name, images in Natural_images_dict.items():
    print(NatImg_name)
    print(len(images))

X, y = [], []

for NatImg_name, images in Natural_images_dict.items():
    for image in images:
        img = cv2.imread(str(image))
        resized_img = cv2.resize(img,(180,180))
        X.append(resized_img)
        y.append(NatImage_labels_dict[NatImg_name])

y[:5]

X[0]

import numpy as np
X =np.asarray(X)

y =np.asarray(y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

len(X_train)

len(X_test)

num_classes=6
model = Sequential([
   layers.experimental.preprocessing.Rescaling(1./255),
  layers.Conv2D(64, 7, activation='relu', padding="same"),
  layers.MaxPooling2D(2),
  layers.Conv2D(128, 3, activation='relu', padding="same"),
  layers.MaxPooling2D(2),
  layers.Conv2D(256, 3, activation='relu', padding="same"),
  layers.Conv2D(256, 3, activation="relu", padding="same"),
  layers.MaxPooling2D(2),
  layers.Flatten(),
  layers.Dense(128, activation="relu"),
  layers.Dropout(0.5),
  layers.Dense(64, activation="relu"),
  layers.Dropout(0.5),
  layers.Dense(6, activation="softmax")
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
              
m=model.fit(X_train, y_train, epochs=30)

model.evaluate(X_test,y_test)

predictions = model.predict(X_test)
predictions

score = tf.nn.softmax(predictions[5])

np.argmax(score)

y_test[0]

N = np.arange(0, 30)
plt.style.use('ggplot')
plt.figure()
plt.plot(N, m.history['loss'], label='train_loss')
plt.plot(N, m.history['val_loss'], label='val_loss')
plt.plot(N, m.history['accuracy'], label='train_accuracy')
plt.plot(N, m.history['val_accuracy'], label='val_accuracy')
plt.title('Training loss and accuracy')
plt.xlabel('Epoch #')
plt.ylabel('Loss/Accuracy')
plt.legend()
plt.show()

model.save_weights('my_model_weights.h5')
model.save('my_model.h5')