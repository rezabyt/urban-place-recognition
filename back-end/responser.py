import json
from classifier import Classifier
import os


class Responser:
    def __init__(self):
        self.num_leading_zeros = 3

        # Load model
        self.classifier = Classifier()
        print('Model loaded.')

        # Load database
        with open('datasets/database.json') as json_file:
            self.database = json.load(json_file)
        print('Database loaded.')

        all_images_directory = './static/images/all/'
        base_class_names = [name for name in os.listdir(all_images_directory)]
        self.class_name_category = {}
        for base_class_name in base_class_names:
            if base_class_name != '.DS_Store':
                class_names = []
                for name in os.listdir(os.path.join(all_images_directory, base_class_name)):
                    if name != '.DS_Store':
                        class_names.append(name)
                self.class_name_category[base_class_name] = class_names

    def get_predicted_classes(self, image_path):
        predicted_classes = self.classifier.predict(image_path)
        results = []
        for class_id in predicted_classes:
            normalized_class_id = str(class_id).zfill(self.num_leading_zeros)
            predicted_class = self.database[normalized_class_id]
            data = {'id': normalized_class_id, 'path': predicted_class['image_path'],
                    'name': predicted_class['place_name']}
            results.append(data)
        return results

    def get_image_detail(self, image_id):
        if image_id not in self.database:
            return 'None'

        base_place_info = self.database[image_id]

        for name in self.class_name_category:
            if image_id in self.class_name_category[name]:
                class_name = name
                break

        gallery = self.get_gallery_names(class_name, image_id)
        similar_places = self.get_similar_places(class_name)
        data = {'place_name': base_place_info['place_name'], 'class_id': base_place_info['class_id'],
                'class_name': base_place_info['class_name'], 'image_path': base_place_info['image_path'],
                'location_path': base_place_info['location_path'], 'description': base_place_info['description'],
                'gallery': gallery,
                'similar_places': similar_places}
        return data

    def get_gallery(self):
        gallery = []
        for class_id in self.database:
            gallery_item = self.database[class_id]
            data = {'id': class_id, 'path': gallery_item['image_path'], 'name': gallery_item['place_name']}
            gallery.append(data)
        return gallery

    def get_gallery_names(self, class_name, image_id):
        gallery_image_names = []
        base_path = './static/images/all/{}/{}'.format(class_name, image_id)
        num_max_image = 7
        for name in os.listdir(base_path):
            if len(gallery_image_names) == num_max_image:
                break

            if name != '.DS_Store':
                gallery_image_names.append(name)

        gallery = []
        for image_name in gallery_image_names:
            image_path = 'http://127.0.0.1:5000/static/images/all/{}/{}/{}'.format(class_name, image_id, image_name)
            gallery.append({'path': image_path})
        return gallery

    def get_similar_places(self, class_name):
        base_path = './static/images/all/{}/'.format(class_name)
        num_max_image = 7
        similar_places = []
        for name in os.listdir(base_path):
            if len(similar_places) == num_max_image:
                break

            if name != '.DS_Store':
                similar_place = self.database[name]
                data = {'id': name, 'path': similar_place['image_path'],
                        'name': similar_place['place_name']}
                similar_places.append(data)

        return similar_places
