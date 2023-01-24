import os
from PIL import Image


def reformat_images(num_classes=56, shape=(224, 224)):
    num_leading_zeros = 3
    raw_size_directory = './datasets/dataset-raw-shape/'

    # Create directory for new dataset.
    new_dataset_directory = './datasets/dataset-shape-{}-{}/'.format(shape[0], shape[1])
    if not os.path.exists(new_dataset_directory):
        os.makedirs(new_dataset_directory)

    for i in range(num_classes):
        current_directory = os.path.join(raw_size_directory, str(i).zfill(num_leading_zeros))

        # Create image directory for new dataset.
        new_directory = os.path.join(new_dataset_directory, str(i).zfill(num_leading_zeros))
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)

        count = 0
        for filename in os.listdir(current_directory):
            img = None
            try:
                img = Image.open(os.path.join(current_directory, filename))
            except:
                print('Can not open the image {} in {} directory.'.format(filename, current_directory))
            if img is not None:
                try:
                    img = img.resize(shape)
                    img.save(os.path.join(new_directory, '{}-{}.png'.format(str(i).zfill(num_leading_zeros),
                                                                            str(count).zfill(num_leading_zeros))))
                    count = count + 1
                except:
                    print('Can not save the image in {} directory'.format(new_directory))


# reformat_images(shape=(224, 224))
