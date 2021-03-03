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

    @staticmethod
    def check_status_code(status_code, request_code):
        assert status_code == request_code

    @staticmethod
    def check_get(url, status_code=200, **kwargs):
        request = requests.get(url=url, **kwargs)
        JSON_PlaceholderAPI.check_status_code(status_code, request.status_code)
        content = request.content.decode(encoding=request.encoding)

        return content

    @staticmethod
    def check_post(url, json_item, status_code=201, **kwargs):
        request = requests.post(url=url, json=json_item, **kwargs)
        JSON_PlaceholderAPI.check_status_code(status_code, request.status_code)
        return request