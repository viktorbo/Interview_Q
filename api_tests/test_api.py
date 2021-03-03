from api_tests.helpers.utils import read_json, list_transform_dict
from api_tests.helpers.json_placeholder_api import JSON_PlaceholderAPI as api
import json
import pytest


class TestGET:
    def test_get_base(self, log):
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

    @pytest.mark.parametrize("n", [1, 55, 100, 0, 101, 'foo', -1, 'fake!@#$%^&*()_+=<>,.;:"/?\|{}[]~`'])
    def test_get_posts_n(self, log, n):
        url = f"{api.POSTS_URL}/{n}"
        status_code = 200
        success_msg = f"GET request to {url} successful!"

        if n in [0, 101, 'foo', -1, 'fake!@#$%^&*()_+=<>,.;:"/?\|{}[]~`']:
            status_code = 404
            expected_result = {}
            success_msg = f"GET request to {url} returned 404 code and empty data!"
        else:
            expected_result = read_json(api.POSTS_JSON)[n - 1]

        content = api.check_get(url, status_code)
        log.info(success_msg)

        assert expected_result == list_transform_dict(content), \
            log.error("Expected data don't equal to data from request!")

    def test_get_posts_n_comments_out(self, log):
        url = f"{api.POSTS_URL}/100500/comments"

        content = api.check_get(url)
        log.info(f"GET request to {url} successful!")

        assert [] == list_transform_dict(content), log.error("Expected data don't equal to data from request!")

    @pytest.mark.parametrize("n", [1, 55, 100, 0, 101, 'foo', -1, 'fake!@#$%^&*()_+=<>,.;:"/?\|{}[]~`'])
    def test_get_post_n_comments(self, log, n):
        url = f"{api.POSTS_URL}/{n}/comments"
        status_code = 200
        success_msg = f"GET request to {url} successful!"
        expected_result = []

        if n in [0, 101, 'foo', -1, 'fake!@#$%^&*()_+=<>,.;:"/?\|{}[]~`']:
            if n == 'fake!@#$%^&*()_+=<>,.;:"/?\|{}[]~`':
                status_code = 404
                expected_result = {}
                success_msg = f"GET request to {url} returned 404 code and empty data!"
        else:
            expected_result = dict(zip(['1', '55', '100'], read_json(api.POST_COMMENTS_JSON)))[f'{n}']
        content = api.check_get(url, status_code)
        log.info(success_msg)

        assert expected_result == list_transform_dict(content), \
            log.error("Expected data don't equal to data from request!")

    def test_get_comments_post_id_negative(self, log):
        url = f"{api.COMMENTS_URL}?postId=100500"

        content = api.check_get(url)
        log.info(f"GET request to {url} successful!")

        assert [] == list_transform_dict(content), log.error("Expected data don't equal to data from request!")

    @pytest.mark.parametrize("n", [1, 55, 100, 0, 101, 'foo', -1, 'fake!@#$%^&*()_+=<>,.;:"/?\|{}[]~`'])
    def test_get_comments_post_id(self, log, n):
        url = f"{api.COMMENTS_URL}?postId={n}"
        success_msg = f"GET request to {url} successful!"
        expected_result = []

        if n not in [0, 101, 'foo', -1, 'fake!@#$%^&*()_+=<>,.;:"/?\|{}[]~`']:
            expected_result = [result for result in read_json(api.COMMENTS_JSON) if result['postId'] == n]

        content = api.check_get(url)
        log.info(success_msg)

        assert expected_result == list_transform_dict(content), \
            log.error("Expected data don't equal to data from request!")


class TestPOST:
    def test_post_posts_normal(self, log):
        fake_post = \
            {
                "userId": 10,
                "title": "Fake",
                "body": "Fake Fake Fake"
            }
        request = api.check_post(url=api.POSTS_URL, json_item=fake_post)
        fake_post.update({'id': 101})
        assert json.loads(request.content) == fake_post, log.error("Request data don't match with input data.")
        log.info(f"POST request to {api.POSTS_URL} with json: {fake_post} successful!")

    def test_post_posts_already_exist(self, log):
        fake_post = \
            {
                "id": 1,
                "userId": 10,
                "title": "fake",
                "body": "fake fake fake"
            }
        request = api.check_post(url=api.POSTS_URL, json_item=fake_post)
        fake_post.update({'id': 101})
        assert json.loads(request.content) == fake_post, log.error("Request data don't match with input data.")
        log.info(f"POST request to {api.POSTS_URL} with json: {fake_post} successful!")

    def test_post_posts_empty(self, log):
        fake_post = \
            {
                "userId": None,
                "title": None,
                "body": None
            }
        request = api.check_post(url=api.POSTS_URL, json_item=fake_post)
        fake_post.update({'id': 101})
        assert json.loads(request.content) == fake_post, log.error("Request data don't match with input data.")
        log.info(f"POST request to {api.POSTS_URL} with json: {fake_post} successful!")

    def test_post_posts_https(self, log):
        url = api.POSTS_URL.replace('http:', 'https:')
        fake_post = \
            {
                "userId": 10,
                "title": "fake",
                "body": "fake fake fake"
            }
        request = api.check_post(url=url, json_item=fake_post)
        fake_post.update({'id': 101})
        assert json.loads(request.content) == fake_post, log.error("Request data don't match with input data.")
        log.info(f"POST request to {url} with json: {fake_post} successful!")

    def test_post_posts_id_over100(self, log):
        fake_post = \
            {
                "id": 105,
                "userId": 10,
                "title": "fake",
                "body": "fake fake fake"
            }
        request = api.check_post(url=api.POSTS_URL, json_item=fake_post)
        fake_post.update({'id': 101})
        assert json.loads(request.content) == fake_post, log.error("Request data don't match with input data.")
        log.info(f"POST request to {api.POSTS_URL} with json: {fake_post} successful!")

    def test_post_posts_id_less0(self, log):
        fake_post = \
            {
                "id": -5,
                "userId": 10,
                "title": "fake",
                "body": "fake fake fake"
            }
        request = api.check_post(url=api.POSTS_URL, json_item=fake_post)
        fake_post.update({'id': 101})
        assert json.loads(request.content) == fake_post, log.error("Request data don't match with input data.")
        log.info(f"POST request to {api.POSTS_URL} with json: {fake_post} successful!")

    def test_post_posts_str_id(self, log):
        fake_post = \
            {
                "userId": 'fake',
                "title": 'fake',
                "body": 'fake'
            }
        request = api.check_post(url=api.POSTS_URL, json_item=fake_post)
        fake_post.update({'id': 101})
        assert json.loads(request.content) == fake_post, log.error("Request data don't match with input data.")
        log.info(f"POST request to {api.POSTS_URL} with json: {fake_post} successful!")

    def test_post_posts_str_id_spec_chars(self, log):
        fake_post = \
            {
                "userId": '!@#$%^&*()_+=<>,.;:"/?\|{}[]~`',
                "title": 'fake',
                "body": 'fake'
            }
        request = api.check_post(url=api.POSTS_URL, json_item=fake_post)
        fake_post.update({'id': 101})
        assert json.loads(request.content) == fake_post, log.error("Request data don't match with input data.")
        log.info(f"POST request to {api.POSTS_URL} with json: {fake_post} successful!")

    def test_post_posts_len_title(self, log):
        fake_post = \
            {
                "userId": 5,
                "title": 300*'s',
                "body": 'fake'
            }
        request = api.check_post(url=api.POSTS_URL, json_item=fake_post)
        fake_post.update({'id': 101})
        assert json.loads(request.content) == fake_post, log.error("Request data don't match with input data.")
        log.info(f"POST request to {api.POSTS_URL} with json: {fake_post} successful!")

    def test_post_posts_spec_chars_title(self, log):
        fake_post = \
            {
                "userId": 5,
                "title": 'fake!@#$%^&*()_+=<>,.;:"/?\|{}[]~`',
                "body": 'fake'
            }
        request = api.check_post(url=api.POSTS_URL, json_item=fake_post)
        fake_post.update({'id': 101})
        assert json.loads(request.content) == fake_post, log.error("Request data don't match with input data.")
        log.info(f"POST request to {api.POSTS_URL} with json: {fake_post} successful!")

    def test_post_posts_len_body(self, log):
        fake_post = \
            {
                "userId": 5,
                "title": 'fake',
                "body": 300*'s'
            }
        request = api.check_post(url=api.POSTS_URL, json_item=fake_post)
        fake_post.update({'id': 101})
        assert json.loads(request.content) == fake_post, log.error("Request data don't match with input data.")
        log.info(f"POST request to {api.POSTS_URL} with json: {fake_post} successful!")

    def test_post_posts_spec_chars_body(self, log):
        fake_post = \
            {
                "userId": 5,
                "title": 'fake',
                "body": 'fake!@#$%^&*()_+=<>,.;:"/?\|{}[]~`'
            }
        request = api.check_post(url=api.POSTS_URL, json_item=fake_post)
        fake_post.update({'id': 101})
        assert json.loads(request.content) == fake_post, log.error("Request data don't match with input data.")
        log.info(f"POST request to {api.POSTS_URL} with json: {fake_post} successful!")
