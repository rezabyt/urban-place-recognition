import requests
import time
import json
import shutil
import re
import os

# Read locations for crawling
f = open('location-for-crawling/locations.json', "r")
locations_for_crawling = json.loads(f.read())

# Crawling locations
for i in locations_for_crawling:
    num_crawled_url = 0
    num_images_in_page = 24
    threshold = 20 * num_images_in_page
    locations = []
    location_name = i['name']
    location_id = i['location_id']
    end_cursor = ''
    end_cursors = []
    has_next_page = True

    print('{}: {}'.format(location_name, location_id))
    while has_next_page:
        end_cursors.append({'end_cursor': end_cursor})
        url = "https://www.instagram.com/explore/locations/{0}/?__a=1&max_id={1}".format(location_id, end_cursor)
        result = requests.get(url)
        try:
            data = json.loads(result.text)
            try:
                # Extract image urls.
                edge_location_to_media = data['graphql']['location']['edge_location_to_media']
                edges = edge_location_to_media['edges']
                for edge in edges:
                    locations.append({'display_url': edge['node']['display_url']})
                    num_crawled_url = num_crawled_url + 1

                # Update next url to crawl.
                page_info = edge_location_to_media['page_info']
                has_next_page = page_info['has_next_page']
                end_cursor = page_info['end_cursor']

                # Print number of crawled images for monitoring.
                print('num_crawled_url:', num_crawled_url)

                # Check the threshold.
                if num_crawled_url >= threshold:
                    break

                # Insurance to not reach a time limit
                time.sleep(2)
            except:
                print('Can not parse json.')
        except:
            print('Can not parse json.')

    # Create directory for location.
    base_path = 'instagram-downloaded-images/{0}/'.format(location_name)
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    # Save end cursors to json file.
    end_cursors_file_name = base_path + '/end_cursors.json'
    with open(end_cursors_file_name, 'w') as outfile:
        json.dump(end_cursors, outfile)

    # Save locations to json file.
    locations_file_name = base_path + '/locations.json'
    with open(locations_file_name, 'w') as outfile:
        json.dump(locations, outfile)

    num_downloaded_image = 0
    for location in locations:
        try:
            image_url = location['display_url']
            result = requests.get(image_url, stream=True)
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            result.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            image_name = re.search(r"/(.*?)\?", image_url).group(1).split('/')[-1]
            image_path = base_path + image_name
            with open(image_path, 'wb') as f:
                shutil.copyfileobj(result.raw, f)
            num_downloaded_image = num_downloaded_image + 1

            if num_downloaded_image % num_images_in_page == 0:
                print('num_downloaded_image:', num_downloaded_image)
            time.sleep(1)
        except:
            print('Can not download image.')
    if num_downloaded_image % num_images_in_page != 0:
        print('num_downloaded_image:', num_downloaded_image)
