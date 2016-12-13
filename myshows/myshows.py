# -*- coding: utf-8 -*-
import requests
import hashlib
import urlparse
import constants
import exceptions
from requests.exceptions import HTTPError


class MyshowsApiBase(object):
    def __init__(self, login=None, password=None, password_md5=None):
        if password and password_md5:
            raise ValueError("Use password OR password_md5")

        if login is None or (password or password_md5) is None:
            raise ValueError("Login and password (password_md5) requred")

        self._credentials = {
            'login': login,
            'password': password_md5 if password_md5 is not None else hashlib.md5(password).hexdigest()
        }

        self.req = requests.Session()
        self._login_path = constants.LOGIN_PATH
        self._login_try()

    def _login_try(self):
        url = urlparse.urljoin(constants.API_HOST, self._login_path)
        self.__api_call(url, self._credentials, not_json=True)

    def __api_call(self, url, data, not_json=False):
        try:
            req = self.req.get(url,
                               params={key: values for key, values in data.iteritems() if
                                       values is not None} if data else {}
                               )

            if req.status_code == 401:
                raise exceptions.MyShowsLoginRequiredException()
            elif req.status_code == 404:
                raise exceptions.MyShowsNotFoundException()
            elif req.status_code == 500:
                raise exceptions.MyShowsInvalidParameter()
        except (HTTPError) as e:
            print e
            raise exceptions.MyShowsException()

        if not_json:
            return req.text
        else:
            return req.json() or {}

    def profile(self):
        url = urlparse.urljoin(constants.API_HOST, constants.PROFILE_PATH)
        return self.__api_call(url, None)

    def shows(self):
        url = urlparse.urljoin(constants.API_HOST, constants.SHOWS_PATH)
        return self.__api_call(url, None)

    def search_file(self, filename):
        url = urlparse.urljoin(constants.API_HOST, constants.SEARCH_EPISODE_PATH)
        data = {
            'q': filename
        }
        return self.__api_call(url, data)

    def search(self, q):
        url = urlparse.urljoin(constants.API_HOST, constants.SEARCH_PATH)
        data = {
            'q': q
        }
        return self.__api_call(url, data)

    def show_id(self, show_id):
        url = urlparse.urljoin(constants.API_HOST, constants.SHOW_ID_PATH)
        url += "%d" % show_id
        return self.__api_call(url, None)

    def genres(self):
        url = urlparse.urljoin(constants.API_HOST, constants.SHOW_ID_PATH)
        return self.__api_call(url, None)

    def check_episode(self, episode_id, rating=None):
        url = urlparse.urljoin(constants.API_HOST, constants.CHECK_PATH)
        url += "%d" % episode_id
        return self.__api_call(url, {'rating': rating}, not_json=True)

    def unwatched(self):
        url = urlparse.urljoin(constants.API_HOST, constants.UNWATCHED_PATH)
        return self.__api_call(url, None)


class MyshowsApiSocial(MyshowsApiBase):
    """Login with social networks"""
    SOCIALS = ['vk', 'fb', 'tw']

    def __init__(self, social, **kwargs):
        """
        http://api.myshows.ru/profile/login/vk?token=<token>&userId=<userId>
        http://api.myshows.ru/profile/login/fb?token=<token>&userId=<userId>
        http://api.myshows.ru/profile/login/tw?token=<token>&userId=<userId>&userId=<secret>
        """

        if social not in self.SOCIALS:
            raise ValueError("Invalid social parameter. Must be in %s" % self.SOCIALS)
        self._login_path = constants.LOGIN_PATH + "/%s" % social
        for item in kwargs.items():
            if not item[1]:
                raise ValueError("Empty %s login parameter" % item[0])
        self._credentials.update(kwargs)
        self._login_try()
