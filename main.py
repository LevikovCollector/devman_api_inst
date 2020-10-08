import requests
from PIL import Image
import os
from urllib3 import disable_warnings, exceptions



def download_img(img_name, img_url):
    if not os.path.exists('images'):
        os.makedirs('images')

    if type(img_url) == list:
        for  img in img_url:
            response = requests.get(img, verify=False)
            response.raise_for_status()

            save_img(f'{img_name}', response.content, file_expansion(img))

    else:
        response = requests.get(img_url, verify=False)
        response.raise_for_status()
        save_img(img_name, response.content, file_expansion(img_url))


def save_img(img_name, img_content, expansion):
    img_index = len(os.listdir('images'))
    file_path = f'images\\{img_name}_{img_index}.{expansion}'

    with open(file_path, 'wb') as file:
        file.write(img_content)
    print(f'Файл: {img_name}_{img_index}.{expansion} - скачен')


def fetch_spacex_last_launch():
    response = requests.get('https://api.spacexdata.com/v3/launches/101')
    response.raise_for_status()
    return (response.json()['links']['flickr_images'])

def file_expansion(file_url):
    return file_url.split('/')[-1].split('.')[-1]

def fetch_hubble(hubble_id):
    response = requests.get(f'http://hubblesite.org/api/v3/image/{hubble_id}')
    response.raise_for_status()

    hubble_images = []
    for hubble_file in response.json()['image_files']:
        file_url = hubble_file['file_url'].replace('//','http://')
        hubble_images.append(file_url)

    download_img(f'img_from_hubble', hubble_images)

def fetch_hubble_collections(collections_name):
    # “holiday_cards”, “wallpaper”, “spacecraft”, “news”, “printshop”, “stsci_gallery”
    response = requests.get(f'http://hubblesite.org/api/v3/images/{collections_name}')
    response.raise_for_status()
    for collection in response.json():
        fetch_hubble(collection['id'])

def convert_to_jpg(folder_with_img):
    if not os.path.exists('images_JPG'):
        os.makedirs('images_JPG')
    all_files_from_dir = os.listdir(folder_with_img)
    for img in all_files_from_dir:
        image_name = img.split('.')[0]
        image = Image.open(f'{folder_with_img}\\{img}')
        width, height  = image.size
        print(f'Размеры до изменений: {image.size}')
        image = image.convert('RGB')
        if width > height:
           width = 1080
        else:
            height = 1080
        image.thumbnail((width, height))
        print(f'Размеры после изменений: {image.size}')
        image.save(f"images_JPG\\{image_name}.jpeg", format="JPEG")
        print(f'Изменен файл: {image_name}')
        print('#'*10)

if __name__ == '__main__':
    disable_warnings(exceptions.InsecureRequestWarning)
    try:
        convert_to_jpg('images')
    except requests.exceptions.HTTPError as error:
        print(f'Возникла ошибка: {error}')
