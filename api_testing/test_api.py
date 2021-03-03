from api_testing.helpers.utils import read_json, list_transform_dict
from api_testing.helpers.json_placeholder_api import JSON_PlaceholderAPI as api
import json
import pytest
from pathlib import Path


class TestGET:
    def test_get(self, log):
        url = api.BASE_URL
        request = api.get(url=url)
        api.check_status_code(200, request.status_code)
        log.info(f"GET request to {url} successful!")

    def test_get_posts(self, log):
        url = api.POSTS_URL
        request = api.get(url=url)
        api.check_status_code(200, request.status_code)
        log.info(f"GET request to {url} successful!")

        content = request.content.decode(encoding=request.encoding)
        expected_result = read_json(api.POSTS_JSON)

        assert expected_result == list_transform_dict(content), \
            log.error("Expected data don't equal to data from request!")

    def test_get_posts_out(self, log):
        url = f"{api.POSTS_URL}/100500"
        request = api.get(url=url)
        api.check_status_code(404, request.status_code)
        log.info(f"GET request to {url} return 400 code. It's expected.")

    @pytest.mark.parametrize("n", [1, 55, 100])
    def test_get_posts_n(self, log, n):
        url = f"{api.POSTS_URL}/{n}"

        request = api.get(url=url)
        api.check_status_code(200, request.status_code)
        log.info(f"GET request to {url} successful!")

        content = request.content.decode(encoding=request.encoding)
        expected_result = read_json(api.POSTS_JSON)[n - 1]

        assert expected_result == list_transform_dict(content), \
            log.error("Expected data don't equal to data from request!")

    def test_get_posts_n_comments_out(self, log):
        url = f"{api.POSTS_URL}/100500/comments"

        request = api.get(url=url)
        api.check_status_code(200, request.status_code)
        log.info(f"GET request to {url} successful!")

        content = request.content.decode(encoding=request.encoding)

        assert [] == list_transform_dict(content), log.error("Expected data don't equal to data from request!")

    @pytest.mark.parametrize("n", [1, 55, 100])
    def test_get_post_n_comments(self, log, n):
        url = f"{api.POSTS_URL}/{n}/comments"

        request = api.get(url=url)
        api.check_status_code(200, request.status_code)
        log.info(f"GET request to {url} successful!")

        content = request.content.decode(encoding=request.encoding)
        expected_result = read_json(api.POST_COMMENTS_JSON)

        assert dict(zip(['1', '55', '100'], expected_result))[f'{n}'] == list_transform_dict(content), \
            log.error("Expected data don't equal to data from request!")

    def test_get_comments_post_id_negative(self, log):
        url = f"{api.COMMENTS_URL}?postId=100500"

        request = api.get(url=url)
        api.check_status_code(200, request.status_code)
        log.info(f"GET request to {url} successful!")

        content = request.content.decode(encoding=request.encoding)

        assert [] == list_transform_dict(content), log.error("Expected data don't equal to data from request!")

    @pytest.mark.parametrize("n", [1, 55, 100])
    def test_get_comments_post_id(self, log, n):
        url = f"{api.COMMENTS_URL}?postId={n}"

        request = api.get(url=url)
        api.check_status_code(200, request.status_code)
        log.info(f"GET request to {url} successful!")

        content = request.content.decode(encoding=request.encoding)
        expected_result = read_json(api.COMMENTS_JSON)
        expected_result = [result for result in expected_result if result['postId'] == n]

        assert expected_result == list_transform_dict(content), \
            log.error("Expected data don't equal to data from request!")


class TestPOST:
    def test_post_comment(self, log):
        url = api.POSTS_URL

        request = api.post(url=url, json=api.comment_fake_json)
        api.check_status_code(201, request.status_code)
        log.info(f"POST request to {url} with json: {api.comment_fake_json} successful!")

        old_content = list(read_json(api.POSTS_JSON))
        content = request.content.decode(encoding=request.encoding)

        assert len(old_content) + 1 == list_transform_dict(content)['id']

