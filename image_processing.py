import requests
from PIL import Image
import os
from urllib3 import disable_warnings, exceptions


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def download_img(img_name, img_url):
    create_folder('images')
    img_urls = []
    if isinstance(img_url, str):
        img_urls.append(img_url)
    else:
        img_urls = img_url

    for index, img in enumerate(img_urls):
        response = requests.get(img, verify=False)
        response.raise_for_status()

        save_img(f'{img_name}_{index}', response.content, get_file_extension(img))

def save_img(img_name, img_content, extension):
    file_path = f'images/{img_name}.{extension}'

    with open(file_path, 'wb') as file:
        file.write(img_content)
    print(f'Файл: {img_name}.{extension} - скачен')

def fetch_spacex_last_launch():
    response = requests.get('https://api.spacexdata.com/v3/launches/101')
    response.raise_for_status()
    return response.json()['links']['flickr_images']

def get_file_extension(file_url):
    return file_url.split('/')[-1].split('.')[-1]

def fetch_hubble_collections(collections_name):
    response = requests.get(f'http://hubblesite.org/api/v3/images/{collections_name}')
    response.raise_for_status()
    collections_img = []
    for collection in response.json():
        response = requests.get(f'http://hubblesite.org/api/v3/image/{collection["id"]}')
        response.raise_for_status()
        for hubble_file in response.json()['image_files']:
            file_url = hubble_file['file_url'].replace('//', 'http://')
            collections_img.append(file_url)

    download_img(f'img_from_hubble', collections_img)

def convert_to_jpg(folder_with_img):
    create_folder('images_JPG')

    all_files_from_dir = os.listdir(folder_with_img)
    for img in all_files_from_dir:
        image_name = img.split('.')[0]
        image = Image.open(f'{folder_with_img}/{img}')
        image = image.convert('RGB')
        image.thumbnail((1080, 1080))
        image.save(f"images_JPG/{image_name}.jpeg", format="JPEG")


if __name__ == '__main__':
    disable_warnings(exceptions.InsecureRequestWarning)
    try:
        fetch_hubble_collections('wallpaper')
        convert_to_jpg('images')
    except requests.exceptions.HTTPError as error:
        print(f'Возникла ошибка: {error}')
