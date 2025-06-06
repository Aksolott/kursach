import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
PICTURES_DIR = os.path.join(ASSETS_DIR, "pictures")

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
FPS = 60