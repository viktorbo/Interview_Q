from api_testing.helpers.utils import read_json, list_transform_dict
from api_testing.helpers.json_placeholder_api import JSON_PlaceholderAPI as api
import json
import pytest
from pathlib import Path


class TestGET:
    def test_get(self):
        request = api.get(url=api.BASE_URL)
        api.check_status_code(200, request.status_code)

    def test_get_posts(self):
        request = api.get(url=api.POSTS_URL)
        api.check_status_code(200, request.status_code)

        content = request.content.decode(encoding=request.encoding)
        expected_result = read_json(api.POSTS_JSON)

        assert expected_result == list_transform_dict(content)

    def test_get_posts_n_negative(self):
        request = api.get(url=f"{api.POSTS_URL}/100500")
        api.check_status_code(404, request.status_code)

    @pytest.mark.parametrize("n", [1, 55, 100])
    def test_get_posts_n(self, n):
        request = api.get(url=f"{api.POSTS_URL}/{n}")
        api.check_status_code(200, request.status_code)

        content = request.content.decode(encoding=request.encoding)
        expected_result = read_json(api.POSTS_JSON)[n - 1]

        assert expected_result == list_transform_dict(content)

    def test_get_posts_n_comments_negative(self):
        request = api.get(url=f"{api.POSTS_URL}/100500/comments")
        api.check_status_code(200, request.status_code)

        content = request.content.decode(encoding=request.encoding)

        assert [] == list_transform_dict(content)

    @pytest.mark.parametrize("n", [1, 55, 100])
    def test_get_post_n_comments(self, n):
        request = api.get(url=f"{api.POSTS_URL}/{n}/comments")
        api.check_status_code(200, request.status_code)

        content = request.content.decode(encoding=request.encoding)
        expected_result = read_json(api.POST_COMMENTS_JSON)

        assert dict(zip(['1', '55', '100'], expected_result))[f'{n}'] == list_transform_dict(content)

    def test_get_comments_post_id_negative(self):
        request = api.get(url=f"{api.COMMENTS_URL}?postId=100500")
        api.check_status_code(200, request.status_code)

        content = request.content.decode(encoding=request.encoding)

        assert [] == list_transform_dict(content)

    @pytest.mark.parametrize("n", [1, 55, 100])
    def test_get_comments_post_id(self, n):
        request = api.get(url=f"{api.COMMENTS_URL}?postId={n}")
        api.check_status_code(200, request.status_code)

        content = request.content.decode(encoding=request.encoding)
        expected_result = read_json(api.COMMENTS_JSON)
        expected_result = [result for result in expected_result if result['postId'] == n]

        assert  expected_result == list_transform_dict(content)


class TestPOST:
    def test_post(self):

        request = api.get(url=api.POSTS_URL)
        api.check_status_code(200, request.status_code)

        request = api.post(url=api.POSTS_URL, json=api.fake_json)
        api.check_status_code(201, request.status_code)

        old_content = list(read_json(api.POSTS_JSON))
        content = request.content.decode(encoding=request.encoding)

        assert  len(old_content) + 1 == list_transform_dict(content)['id']