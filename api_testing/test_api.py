from api_testing.helpers.utils import read_json, list_transform_dict
from api_testing.helpers.json_placeholder_api import JSON_PlaceholderAPI as api
import json
import pytest
from pathlib import Path


class TestGET:
    def test_get(self, log):
        url = api.BASE_URL
        api.check_get(url)
        log.info(f"GET request to {url} successful!")

    def test_get_posts(self, log):
        url = api.POSTS_URL

        content = api.check_get(url)
        log.info(f"GET request to {url} successful!")

        expected_result = read_json(api.POSTS_JSON)

        assert expected_result == list_transform_dict(content), \
            log.error("Expected data don't equal to data from request!")

    def test_get_posts_out(self, log):
        url = f"{api.POSTS_URL}/100500"
        api.check_get(url=url, status_code=404)
        log.info(f"GET request to {url} return 404 code. It's expected.")

    @pytest.mark.parametrize("n", [1, 55, 100])
    def test_get_posts_n(self, log, n):
        url = f"{api.POSTS_URL}/{n}"

        content = api.check_get(url)
        log.info(f"GET request to {url} successful!")

        expected_result = read_json(api.POSTS_JSON)[n - 1]

        assert expected_result == list_transform_dict(content), \
            log.error("Expected data don't equal to data from request!")

    def test_get_posts_n_comments_out(self, log):
        url = f"{api.POSTS_URL}/100500/comments"

        content = api.check_get(url)
        log.info(f"GET request to {url} successful!")

        assert [] == list_transform_dict(content), log.error("Expected data don't equal to data from request!")

    @pytest.mark.parametrize("n", [1, 55, 100])
    def test_get_post_n_comments(self, log, n):
        url = f"{api.POSTS_URL}/{n}/comments"

        content = api.check_get(url)
        log.info(f"GET request to {url} successful!")

        expected_result = read_json(api.POST_COMMENTS_JSON)

        assert dict(zip(['1', '55', '100'], expected_result))[f'{n}'] == list_transform_dict(content), \
            log.error("Expected data don't equal to data from request!")

    def test_get_comments_post_id_negative(self, log):
        url = f"{api.COMMENTS_URL}?postId=100500"

        content = api.check_get(url)
        log.info(f"GET request to {url} successful!")

        assert [] == list_transform_dict(content), log.error("Expected data don't equal to data from request!")

    @pytest.mark.parametrize("n", [1, 55, 100])
    def test_get_comments_post_id(self, log, n):
        url = f"{api.COMMENTS_URL}?postId={n}"

        content = api.check_get(url)
        log.info(f"GET request to {url} successful!")

        expected_result = read_json(api.COMMENTS_JSON)
        expected_result = [result for result in expected_result if result['postId'] == n]

        assert expected_result == list_transform_dict(content), \
            log.error("Expected data don't equal to data from request!")


class TestPOST:
    def test_post_post(self, log):
        api.check_post(url=api.POSTS_URL, json_item=api.fake_post)
        log.info(f"POST request to {api.POSTS_URL} with json: {api.fake_post} successful!")

    def test_post_comment(self, log):
        api.check_post(url=api.COMMENTS_URL, json_item=api.fake_comment)
        log.info(f"POST request to {api.COMMENTS_URL} with json: {api.fake_comment} successful!")

    def test_post_album(self, log):
        api.check_post(url=api.ALBUMS_URL, json_item=api.fake_album)
        log.info(f"POST request to {api.ALBUMS_URL} with json: {api.fake_album} successful!")

    def test_post_photo(self, log):
        api.check_post(url=api.PHOTOS_URL, json_item=api.fake_photo)
        log.info(f"POST request to {api.PHOTOS_URL} with json: {api.fake_photo} successful!")

    def test_post_todos(self, log):
        api.check_post(url=api.TODOS_URL, json_item=api.fake_todo)
        log.info(f"POST request to {api.TODOS_URL} with json: {api.fake_todo} successful!")

    def test_post_user(self, log):
        api.check_post(url=api.USERS_URL, json_item=api.fake_user)
        log.info(f"POST request to {api.USERS_URL} with json: {api.fake_user} successful!")

