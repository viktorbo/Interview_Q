from pathlib import Path
import requests
import os


class JSON_PlaceholderAPI:

    BASE_URL = "http://jsonplaceholder.typicode.com"
    JSON_DIR = os.getenv('JSON_DIR')

    POSTS_URL = BASE_URL + '/posts'
    POSTS_JSON = (Path(JSON_DIR) / 'posts.json').as_posix()

    COMMENTS_URL = BASE_URL + '/comments'
    COMMENTS_JSON = (Path(JSON_DIR) / 'comments.json').as_posix()
    POST_COMMENTS_JSON = (Path(JSON_DIR) / 'posts_comments.json').as_posix()
    comment_fake_json = \
        {
            "userId": 10,
            "title": "fake",
            "body": "fake"
        }

    @staticmethod
    def check_status_code(status_code, request_code):
        assert status_code == request_code

    @staticmethod
    def get(url):
        return requests.get(url=url)

    @staticmethod
    def post(url, json, **kwargs):
        return requests.post(url=url, json=json, **kwargs)