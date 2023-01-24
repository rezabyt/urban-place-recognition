import tensorflow as tf
import cv2
import numpy as np
from keras.applications.resnet50 import preprocess_input


class Classifier:
    def __init__(self):
        # Load model
        # model_path = './urban-place-recognition-saved-model/model-15-epochs-57-classes-transfer-learning'
        model_path = './urban-place-recognition-saved-model/model-15-epochs-57-classes-with-test-valid-data-set-transfer-learning'
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, image_path):
        # Step 1: read image
        original_image = cv2.imread(image_path)
        if original_image is None:
            return 'None'
        # Resize the image
        resized_image = cv2.resize(original_image, (224, 224))
        # Normalize the image.
        # normalized_image = resized_image / 255

        normalized_image = preprocess_input(resized_image)

        # Step 2: Prediction of the model
        predict_result = self.model.predict_on_batch(np.array([normalized_image]))[0]
        # predict_confidence = [np.max(x) for x in predict_result][0]
        # normalized_predict_confidence = "{:.2f}".format(predict_confidence)
        # predict_class = np.array([np.argmax(x) for x in predict_result])
        # print('predict_class:', predict_class)
        predict_classes = predict_result.argsort()[-6:][::-1]
        return predict_classes

    def build(self):
        return None


# classifier = Classifier()
# print("Classifier loaded.")
# while True:
#     image_name = input()
#     print(classifier.predict('./uploads/' + image_name))
