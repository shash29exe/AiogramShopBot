from os import getenv
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = getenv('TOKEN')
MANAGER_ID = int(os.getenv('MANAGER_ID'))
MANAGER_USERNAME = os.getenv('MANAGER_USERNAME')
MEDIA_ROOT = r'C:\Users\Shash29\PycharmProjects\AiogramShopBot\media'