import tensorflow as tf
import os
import cv2
import numpy as np

# Load model
model_path = './urban-place-recognition-saved-model/model-60-epochs'
model = tf.keras.models.load_model(model_path)
print('Model loaded.')

num_leading_zeros = 3
num_classes = 49
result_directory = './result/'
for i in range(0, num_classes):
    current_directory = result_directory + str(i).zfill(num_leading_zeros)
    if not os.path.exists(current_directory):
        os.makedirs(current_directory)

# It shows how many images are in each class.
count_dictionary = {}
for i in range(0, 49):
    count_dictionary[i] = 0

shape = (224, 224)
test_directory = './uploads/'
num_images = 0
for folder_name in os.listdir(test_directory):
    print(folder_name)
    class_id = folder_name.split('-')[0]
    for filename in os.listdir(os.path.join(test_directory, folder_name)):
        if filename == 'end_cursors.json' or filename == 'locations.json':
            continue
        original_img = cv2.imread(os.path.join(test_directory, folder_name, filename))
        if original_img is not None:
            num_images = num_images + 1
            # Step 1: Prepare the image.
            # Resize the image
            resized_image = cv2.resize(original_img, shape)
            # Normalize the image.
            normalized_image = resized_image / 255

            # Step 2: Prediction of the model
            predict_result = model.predict_on_batch(np.array([normalized_image]))
            predict_confidence = [np.max(x) for x in predict_result][0]
            normalized_predict_confidence = "{:.2f}".format(predict_confidence)
            predict_class = [np.argmax(x) for x in predict_result][0]

            # Step 3: Save image
            target_directory = result_directory + str(predict_class).zfill(num_leading_zeros)
            image_number = count_dictionary[predict_class]
            image_name = '[{}]{}-{}.png'.format(normalized_predict_confidence,
                                                str(image_number).zfill(num_leading_zeros), class_id)
            cv2.imwrite(os.path.join(target_directory, image_name), original_img)

            # Step 4: Update the state of number of images in each class
            count_dictionary[predict_class] = count_dictionary[predict_class] + 1

print('All images:', num_images)
print('Images per classes:', count_dictionary)

print("Finished")
