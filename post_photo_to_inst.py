from instabot import Bot
from dotenv import load_dotenv
import os
import time
import shutil

FOLDER_WITH_IMG='images_JPG'

def public_photo_to_inst(login, password):
    if os.path.exists('config'):
        shutil.rmtree('config')

    bot= Bot()
    bot.login(username=login, password=password)
    all_files_from_dir = os.listdir(FOLDER_WITH_IMG)
    for img in all_files_from_dir:
        bot.upload_photo(f'{FOLDER_WITH_IMG}/{img}', caption='Description')
        if bot.api.last_response.status_code != 200:
            break
        time.sleep(10)


if __name__ == '__main__':
    load_dotenv(dotenv_path='config.env')
    login = os.getenv('INST_LOGIN')
    password = os.getenv('INST_PASS')
    public_photo_to_inst(login, password)