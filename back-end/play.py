import os

all_images_directory = './static/images/all/'
base_class_names = [name for name in os.listdir(all_images_directory)]

class_name_category = {}
for base_class_name in base_class_names:
    if base_class_name != '.DS_Store':
        class_names = []
        for name in os.listdir(os.path.join(all_images_directory, base_class_name)):
            if name != '.DS_Store':
                class_names.append(name)
        class_name_category[base_class_name] = class_names

print(class_name_category)

image_id = '036'
class_name = 'ketabkhane'

gallery_names = []
base_path = './static/images/all/{}/{}'.format(class_name, image_id)
num_max_image = 7
for name in os.listdir(base_path):
    if len(gallery_names) == num_max_image:
        break

    if name != '.DS_Store':
        gallery_names.append(name)

print(gallery_names)
