import datetime, pytz, time
import json
import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv
# from requests_oauthlib import OAuth1Session
# import oauth2 as oauth
# import user_list

def lambda_handler(event, lambda_context) -> None:
    with TwitterApi() as ta:
        user_id_list_obj = user_list.UserList()
        user_id_list = user_id_list_obj.ids()
        user_id = user_id_list[0]
        ta.get_tweet(user_id)
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
        if response.status == 200:
            json_str = data.decode('utf-8')
            array_aa = json.loads(json_str)

            for tweet_info in array_aa:
                print(self.change_time(tweet_info['created_at']))
                print(tweet_info['text'])

    def change_time(self, created_at):
        """[summary]

        Args:
            created_at ([type]): [description]

        Returns:
            [type]: [description]
        """
        # time.struct_time?????????
        st = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
        # datetime?????????(timezone?????????)
        utc_time = datetime.datetime(
            st.tm_year,
            st.tm_mon,
            st.tm_mday,
            st.tm_hour,
            st.tm_min,
            st.tm_sec,
            tzinfo=datetime.timezone.utc
        )
        # ?????????????????????
        jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
        # ??????????????????
        str_time = jst_time.strftime("%Y-%m-%d %H:%M:%S")
        return str_time

if __name__ == '__main__':
    lambda_handler({}, '')
