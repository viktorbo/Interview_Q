import requests
from api_testing.helpers.utils import read_json
from api_testing.helpers.urls import URL
import json
import pytest
from pathlib import Path


class TestGET:
    def test_get(self):
        request = requests.get(url=URL.jsonplaceholder)
        assert 200 == request.status_code, f"Bad request. Code [{request.status_code}]"

    def test_get_posts(self):
        request = requests.get(url=URL.jsonplaceholder_posts)
        assert 200 == request.status_code, f"Bad request. Code [{request.status_code}]"

        content = request.content.decode(encoding=request.encoding)
        expected_result = read_json(
            '/home/viktorbo/localdata/repos/Interview_Quotes/api_testing/helpers/jsons/posts.json')

        assert expected_result == json.loads(content, encoding=request.encoding), "Wrong data!"

    def test_get_posts_n_negative(self):
        request = requests.get(url=f"{URL.jsonplaceholder_posts}/100500")
        assert 404 == request.status_code, "Status code 200, but expect 404."

    @pytest.mark.parametrize("n", [1, 55, 100])
    def test_get_posts_n(self, n):
        request = requests.get(url=f"{URL.jsonplaceholder_posts}/{n}")
        assert 200 == request.status_code, f"Bad request. Code [{request.status_code}]"

        content = request.content.decode(encoding=request.encoding)
        expected_result = \
            read_json('/home/viktorbo/localdata/repos/Interview_Quotes/api_testing/helpers/jsons/posts.json')[n - 1]

        assert expected_result == json.loads(content, encoding=request.encoding), "Wrong data!"

    def test_get_posts_n_comments_negative(self):
        request = requests.get(url=f"{URL.jsonplaceholder_posts}/100500/comments")
        assert 200 == request.status_code

        content = request.content.decode(encoding=request.encoding)

        assert [] == json.loads(content, encoding=request.encoding), "Request content not empty, but empty is expected."

    @pytest.mark.parametrize("n", [1, 55, 100])
    def test_get_post_n_comments(self, n):
        request = requests.get(url=f"{URL.jsonplaceholder_posts}/{n}/comments")
        assert 200 == request.status_code, f"Bad request. Code [{request.status_code}]"

        content = request.content.decode(encoding=request.encoding)
        expected_result = read_json(
            '/home/viktorbo/localdata/repos/Interview_Quotes/api_testing/helpers/jsons/posts_comments.json')

        assert dict(zip(['1', '55', '100'], expected_result))[f'{n}'] == json.loads(content,
                                                                                    encoding=request.encoding), "Wrong data!"

    def test_get_comments_post_id_negative(self):
        request = requests.get(url=f"{URL.jsonplaceholder_comments}?postId=100500")
        assert 200 == request.status_code, f"Bad request. Code [{request.status_code}]"

        content = request.content.decode(encoding=request.encoding)

        assert [] == json.loads(content), "Request content not empty, but empty is expected."

    @pytest.mark.parametrize("n", [1, 55, 100])
    def test_get_comments_post_id(self, n):
        request = requests.get(url=f"{URL.jsonplaceholder_comments}?postId={n}")
        assert 200 == request.status_code, f"Bad request. Code [{request.status_code}]"

        content = request.content.decode(encoding=request.encoding)
        expected_result = read_json((Path.cwd() / 'helpers' / 'jsons' / 'comments.json').as_posix())
        expected_result = [result for result in expected_result if result['postId'] == n]

        assert json.loads(content) == expected_result, "Wrong data!"


class TestPOST:
    def test_post(self):
        fake_json = \
            {
                "userId": 10,
                "id": 101,
                "title": "fake",
                "body": "fake"
            }

        request = requests.get(url=URL.jsonplaceholder_posts)
        assert 200 == request.status_code, f"Bad request. Code [{request.status_code}]"

        request = requests.post(url=URL.jsonplaceholder_posts, json=fake_json)
        assert 201 == request.status_code, f"Bad request. Code [{request.status_code}]"

        old_content = list(read_json('/home/viktorbo/localdata/repos/Interview_Quotes/api_testing/helpers/jsons/posts.json'))

        assert json.loads(request.content.decode(encoding=request.encoding))['id'] == len(old_content) + 1