from instabot import Bot
from dotenv import load_dotenv
import os
import time
import shutil
from image_processing import create_file_path

FOLDER_WITH_IMG='images_JPG'

def publish_photo_to_inst(login, password):
    bot= Bot()
    bot.login(username=login, password=password)
    all_files_from_dir = os.listdir(FOLDER_WITH_IMG)
    for img in all_files_from_dir:
        bot.upload_photo(create_file_path(FOLDER_WITH_IMG, f'{img}'), caption='Description')
        if bot.api.last_response.status_code != 200:
            break
        time.sleep(10)


if __name__ == '__main__':
    load_dotenv(dotenv_path='config.env')
    if os.path.exists('config'):
        shutil.rmtree('config')
    login = os.getenv('INST_LOGIN')
    password = os.getenv('INST_PASS')
    public_photo_to_inst(login, password)