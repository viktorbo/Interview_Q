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

    ALBUMS_URL = BASE_URL + '/albums'

    PHOTOS_URL = BASE_URL + '/photos'

    TODOS_URL = BASE_URL + '/todos'

    USERS_URL = BASE_URL + '/users'

    fake_post = \
        {
            "userId": 10,
            "title": "fake",
            "body": "fake fake fake"
        }

    fake_comment = \
        {
            "postId": 21,
            "name": "fake",
            "email": "fake@fake.tv",
            "body": "fake fake fake"
        }

    fake_album = \
        {
            "userId": 1,
            "title": "fake fake fake"
        }

    fake_photo = \
        {
            "albumId": 1,
            "title": "fake fake fake",
            "url": "https://via.placeholder.com/600/92c952",
            "thumbnailUrl": "https://via.placeholder.com/150/92c952"
        }

    fake_todo = \
        {
            "userId": 1,
            "title": "fake fake fake",
            "completed": False
        }

    fake_user = \
        {
            "name": "Fake Fake",
            "username": "JOJA",
            "email": "fake@april.biz",
            "address": {
                "street": "Kulas Light",
                "suite": "Apt. 556",
                "city": "Sarovsk",
                "zipcode": "92998-3874",
                "geo": {
                    "lat": "-37.3159",
                    "lng": "81.1496"
                }
            },
            "phone": "1-800-555-35-35",
            "website": "hildegard.org",
            "company": {
                "name": "Company",
                "catchPhrase": "Multi-layered client-server neural-net",
                "bs": "harness real-time e-markets"
            }
        }

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
    def check_post(url, json_item, **kwargs):
        request = requests.post(url=url, json=json_item, **kwargs)
        JSON_PlaceholderAPI.check_status_code(201, request.status_code)
