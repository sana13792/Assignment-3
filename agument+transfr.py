# -*- coding: utf-8 -*-
"""Agument+Transfr.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WEWP0memE7im1Wt9DkaFqEyi4AX3zbRg
"""

from google.colab import drive
drive.mount('/content/gdrive')

import zipfile
with zipfile.ZipFile("/content/gdrive/MyDrive/seg_train.zip","r") as zip_ref:
    zip_ref.extractall("targetdir")

import zipfile
with zipfile.ZipFile("/content/gdrive/MyDrive/Test_data.zip","r") as zip_ref:
    zip_ref.extractall("testdir")

!dir /content/gdrive/MyDrive/seg_train.zip

!dir /content/gdrive/MyDrive/seg_train.zip

import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import tensorflow_datasets as tfds
import pathlib
data_dir = pathlib.Path("data")
data_dir = data_dir.joinpath('/content/targetdir/seg_train')
data_dir
batch_size = 100
img_height = 224
img_width = 224
Channels=3

train_ds = tf.keras.preprocessing.image_dataset_from_directory(  
data_dir,
 subset="training",
 validation_split=0.2,
  seed=123,
  image_size=(224,224),
  batch_size=batch_size)
print(len(train_ds))

target_dict={k: v for v, k in enumerate(np.unique(train_ds.class_names))}
target_dict

source_dict={k: v for v, k in enumerate(np.unique(train_ds.class_names))}
source_val=  [source_dict[train_ds.class_names[i]] for i in range(len(train_ds.class_names))]

train_ds.class_names

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size
     )

class_names = train_ds.class_names

data_dir = pathlib.Path("data")
data_dir = data_dir.joinpath('/content/testdir/seg_pred/seg_pred')
data_dir

test_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(class_names[labels[i]])
        plt.axis("off")

from tensorflow.keras import layers
normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)

import tensorflow as tf
num_classes = 6

model = tf.keras.Sequential([
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

model.compile(
  optimizer='adam',
  loss="sparse_categorical_crossentropy",
  metrics=['accuracy'])

history=model.fit(
  train_ds,
  validation_data=val_ds,
  
  epochs=30

)

test=model.evaluate(test_ds)

N = np.arange(0, 30)
plt.style.use('ggplot')
plt.figure()
plt.plot(N, history.history['loss'], label='train_loss')
plt.plot(N, history.history['val_loss'], label='val_loss')
plt.plot(N, history.history['accuracy'], label='train_accuracy')
plt.plot(N, history.history['val_accuracy'], label='val_accuracy')
plt.title('Training loss and accuracy')
plt.xlabel('Epoch #')
plt.ylabel('Loss/Accuracy')
plt.legend()
plt.show()

predictions = model.predict(val_ds)
predictions

score = tf.nn.softmax(predictions[0])

np.argmax(score)

target_dict={k: v for v, k in enumerate(np.unique(test_ds.class_names))}
target_val=  [target_dict[test_ds.class_names[i]] for i in range(len(test_ds.class_names))]

target_dict={k: v for v, k in enumerate(np.unique(test_ds.class_names))}
target_dict

test_ds.class_names

model.summary()

model.save_weights('my_model_weights.h5')
model.save('my_model.h5')



"""# With data agumentation and transfer learning"""

data_augmentation = tf.keras.Sequential([
  layers.experimental.preprocessing.RandomFlip("horizontal_and_vertical"),
  layers.experimental.preprocessing.RandomRotation(0.2),
])

preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input

rescale = tf.keras.layers.experimental.preprocessing.Rescaling(1./127.5, offset= -1)

base_model = tf.keras.applications.MobileNetV2(include_top=False, weights='imagenet')

image_batch, label_batch = next(iter(train_ds))
feature_batch = base_model(image_batch)
print(feature_batch.shape)

base_model.trainable = False

base_model.summary()

base_model.save_weights('pretrained_modelweights.h5')
base_model.save('pretrained_model.h5')

from google.colab import files
files.download('pretrained_modelweights.h5')
files.download('pretrained_model.h5')

global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
feature_batch_average = global_average_layer(feature_batch)
print(feature_batch_average.shape)

prediction_layer = tf.keras.layers.Dense(6)
prediction_batch = prediction_layer(feature_batch_average)
print(prediction_batch.shape)

inputs = tf.keras.Input(shape=(224, 224, 3))
x = data_augmentation(inputs)
x = preprocess_input(x)
x = base_model(x, training=False)
x = global_average_layer(x)
x = tf.keras.layers.Dropout(0.2)(x)
outputs = prediction_layer(x)
model = tf.keras.Model(inputs, outputs)

base_learning_rate = 0.0001
model.compile(optimizer=tf.keras.optimizers.Adam(lr=base_learning_rate),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

initial_epochs = 10

history = model.fit(train_ds,
                    epochs=10,
                    validation_data=val_ds)

print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()



base_model.trainable = True

fine_tune_at = 100

for layer in base_model.layers[:fine_tune_at]:
    layer.trainable =  False

model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              optimizer = tf.keras.optimizers.RMSprop(lr=base_learning_rate/10),
              metrics=['accuracy'])

fine_tune_epochs = 10
total_epochs =  10 + fine_tune_epochs

history_fine = model.fit(train_ds,
                         epochs=total_epochs,
                         initial_epoch=history.epoch[-1],
                         validation_data=val_ds)

model.evaluate(test_ds)

print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

model.save_weights('my_finalmodel_weights.h5')
model.save('my_finalmodel.h5')

model.save_weights('my_model2_weights.h5')
model.save('my_model2.h5')