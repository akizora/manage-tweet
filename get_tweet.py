import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv

def lambda_handler(event, lambda_context) -> None:
    with GetTweet() as gt:
        sys.exit()

class GetTweet():
    def __init__(self) -> None:
        print('Start')
        load_dotenv(verbose=True)
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
        self.CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
        self.ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
        self.ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        print('End')

if __name__ == '__main__':
     lambda_handler({}, '')
