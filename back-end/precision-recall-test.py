import tensorflow as tf
import os
import cv2
import numpy as np
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


def convert_to_one_hot(label, num_classes):
    return np.eye(num_classes)[label.reshape(-1)].T


# Load model
model_path = './urban-place-recognition-saved-model/model-60-epochs'
model = tf.keras.models.load_model(model_path)
print('Model loaded.')

num_leading_zeros = 3
num_classes = 49
base_path = './test-model-for-thesis/'
shape = (224, 224)

x_images_original = []
y_images_original = []
num_all_image = 0
for class_num in range(num_classes):
    print('Current class:', class_num)
    current_images = []
    current_directory = os.path.join(base_path, str(class_num).zfill(num_leading_zeros))
    for filename in os.listdir(current_directory):
        if filename == 'end_cursors.json' or filename == 'locations.json':
            continue

        original_img = cv2.imread(os.path.join(current_directory, filename))
        if original_img is not None:
            num_all_image = num_all_image + 1
            print(num_all_image)
            print()
            resized_image = cv2.resize(original_img, shape)
            x_images_original.append(resized_image)
            y_images_original.append(class_num)

# normalize image vectors
x_images = np.array(x_images_original)
x_images = x_images / 255.

y_images = np.array(y_images_original)
y_images = convert_to_one_hot(y_images, num_classes).T

y_pred_orig = model.predict_on_batch(x_images)
y_pred = [np.argmax(x) for x in y_pred_orig]

print('Number of images:', num_all_image)

labels = [i for i in range(num_classes)]

# calculate prediction
precision = precision_score(y_images_original, y_pred, labels=labels, average='micro')
print('Precision: %.3f' % precision)

# calculate recall
recall = recall_score(y_images_original, y_pred, labels=labels, average='micro')
print('Recall: %.3f' % recall)
