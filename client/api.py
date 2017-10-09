import requests
from exceptions import Http500Exception, Http404Exception

class Api(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def _url(self, url_path):
        return self.base_url + url_path

    def _accept_header(self, data_format):
        if data_format == 'json':
            return {'Accept': 'application/json'}
        elif data_format == 'html':
            return {'Accept': 'text/html'}
        elif data_format == 'response':
            return {}
        else:
            raise Exception("Invalid Format {}".format(data_format))

    def _response_data(self, response, data_format):
        if response.status_code == 200:
            if data_format == 'response':
                return response
            elif data_format == 'json':
                return response.json()
            elif data_format == 'html':
                return response.text
            else:
                raise Exception("Invalid Format {}".format(data_format))
        elif response.status_code == 404:
            raise Http404Exception()
        elif response.status_code == 500:
            raise Http500Exception()

    def get_users(self, data_format='json'):
        accept_header = self._accept_header(data_format)
        response = requests.get(self._url('/user'), headers=accept_header)
        return self._response_data(response, data_format)

    def get_user(self, user_id, data_format='json'):
        accept_header = self._accept_header(data_format)
        response = requests.get(self._url('/user/{}'.format(user_id)), headers=accept_header)
        return self._response_data(response, data_format)

    def get_posts(self, data_format='json'):
        accept_header = self._accept_header(data_format)
        response = requests.get(self._url('/post'), headers=accept_header)
        return self._response_data(response, data_format)

    def get_post(self, post_id, data_format='json'):
        accept_header = self._accept_header(data_format)
        response = requests.get(self._url('/post/{}'.format(post_id)), headers=accept_header)
        return self._response_data(response, data_format)

    def create_post(self, title, body, author_id, data_format='json'):
        accept_header = self._accept_header(data_format)
        data = {'title': title, 'body': body, 'author_id': author_id}
        response = requests.post(self._url('/post'), data=data, headers=accept_header)
        return self._response_data(response, data_format)
