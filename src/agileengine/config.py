import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    AGILEENGINE_API_KEY = os.getenv('AGILEENGINE_API_KEY')
