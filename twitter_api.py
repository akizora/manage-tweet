import json
import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session
import oauth2 as oauth
import user_list

def lambda_handler(event, lambda_context) -> None:
    with TwitterApi() as ta:
        user_id_list_obj = user_list.UserList()
        user_id_list = user_id_list_obj.ids()
        print(str(user_id_list))
        sys.exit()

class TwitterApi():
    def __init__(self) -> None:
        print('Start')
        load_dotenv(verbose=True)
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
        self.CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
        self.ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
        self.ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
        self.consumer = oauth.Consumer(key=self.CONSUMER_KEY, secret=self.CONSUMER_SECRET)
        self.access_token = oauth.Token(key=self.ACCESS_TOKEN, secret=self.ACCESS_TOKEN_SECRET)
        self.client = oauth.Client(self.consumer, self.access_token)

        self.USER_TIMELINE_URL = "https://api.twitter.com/1.1/statuses/user_timeline.json?user_id="

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        print('End')
    
    def get_tweet(self, user_id):
        """[Get Timeline Tweet]

        Args:
            user_id ([str]): [description]
        """
        nnx = 10
        url = self.USER_TIMELINE_URL + user_id + "&count=" + str(nnx)
        array_aa = []
        response, data = self.client.request(url)
        json_str = data.decode('utf-8')
        array_aa = json.loads(json_str)

        print(array_aa)

if __name__ == '__main__':
     lambda_handler({}, '')
