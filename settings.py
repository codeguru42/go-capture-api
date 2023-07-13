from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent

MEDIA_ROOT = env.path("MEDIA_ROOT")
MEDIA_ROOT.mkdir(exist_ok=True)

IMAGES_DIR = MEDIA_ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)

SGF_DIR = MEDIA_ROOT / "sgf"
SGF_DIR.mkdir(exist_ok=True)

FIREBASE_CREDENTIALS_FILE = BASE_DIR / env.str("FIREBASE_CREDENTIALS_FILE")
