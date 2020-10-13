from instabot import Bot
from dotenv import load_dotenv
import os
import time
import shutil

FOLDER_WITH_IMG='images_JPG'

def public_photo_to_inst():
    if os.path.exists('config'):
        shutil.rmtree('config')

    bot= Bot()
    bot.login(username=os.getenv('INST_LOGIN'), password=os.getenv('INST_PASS'))
    all_files_from_dir = os.listdir(FOLDER_WITH_IMG)
    for img in all_files_from_dir:
        bot.upload_photo(f'{FOLDER_WITH_IMG}/{img}', caption='Description')
        if bot.api.last_response.status_code != 200:
            print(bot.api.last_response)
            break
        time.sleep(10)


if __name__ == '__main__':
    load_dotenv(dotenv_path='config.env')
    public_photo_to_inst()