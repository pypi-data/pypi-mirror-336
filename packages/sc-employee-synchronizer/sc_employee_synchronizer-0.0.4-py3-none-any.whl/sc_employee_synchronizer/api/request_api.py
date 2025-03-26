#  The MIT License (MIT)
#
#  Copyright (c) 2022. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.


import logging
from urllib.parse import urljoin

import requests
import urllib3

from sc_employee_synchronizer.exception import exceptions


class RequestClient(object):
    """
    A class to interact with Http
    """

    def __init__(self, *, url, username=None, password=None, x509_verify=True):
        """
        Create a RequestClient object.

        :param url: the request url.
        :param username: the user name.
        :param password: password.
        :param x509_verify: Whether to validate the x509 certificate when using https
        """
        self._url = url
        self._username = username
        self._password = password
        self._x509_verify = x509_verify

    @property
    def url(self):
        """
        Current username.

        :rtype: str
        """
        return self._url

    @property
    def username(self):
        """
        Current username.

        :rtype: str
        """
        return self._username

    @property
    def password(self):
        """
        Current password.

        :rtype: str
        """
        return self._password

    @property
    def x509_verify(self):
        """
        Whether to validate the x509 certificate when using https

        :rtype: str
        """
        return self._x509_verify

    def http_request(self, method, endpoint, **kwargs):
        """
        Performs a HTTP request to the Nexus REST API on the specified
        endpoint.

        :param method: one of ``get``, ``put``, ``post``, ``delete``.
        :type method: str
        :param endpoint: URI path to be appended to the service URL.
        :type endpoint: str
        :param kwargs: as per :py:func:`requests.request`.
        :rtype: requests.Response
        """
        url = urljoin(self._url, endpoint)

        try:
            response = requests.request(
                method=method, auth=(self._username, self._password), url=url,
                verify=self._x509_verify, timeout=(3.15, 27), **kwargs)
        except requests.exceptions.ConnectionError as e:
            logging.error("failed to connect to %s, cause: %s", url, e)
            raise exceptions.HttpClientAPIError(e)
        except urllib3.exceptions.ReadTimeoutError as e:
            logging.error("read timeout error to %s, cause: %s", url, e)
            raise exceptions.HttpClientAPIError(e)
        except requests.exceptions.ReadTimeout as e:
            logging.error("read timeout to %s, cause: %s", url, e)
            raise exceptions.HttpClientAPIError(e)

        if response.status_code == 400:
            raise exceptions.BadRequestException(response.text)

        if response.status_code == 401:
            raise exceptions.HttpClientInvalidCredentials("Invalid credential {0}, {1}".format(
                self._username, self._password))

        return response

    def http_get(self, endpoint):
        """
        Performs a HTTP GET request on the given endpoint.

        :param endpoint: name of the Nexus REST API endpoint.
        :type endpoint: str
        :rtype: requests.Response
        """
        return self.http_request('get', endpoint, stream=True)

    def http_head(self, endpoint):
        """
        Performs a HTTP HEAD request on the given endpoint.

        :param endpoint: name of the Nexus REST API endpoint.
        :type endpoint: str
        :rtype: requests.Response
        """
        return self.http_request('head', endpoint)

    def http_post(self, endpoint, **kwargs):
        """
        Performs a HTTP POST request on the given endpoint.

        :param endpoint: name of the Nexus REST API endpoint.
        :type endpoint: str
        :param kwargs: as per :py:func:`requests.request`.
        :rtype: requests.Response
        """
        return self.http_request('post', endpoint, **kwargs)

    def http_put(self, endpoint, **kwargs):
        """
        Performs a HTTP PUT request on the given endpoint.

        :param endpoint: name of the Nexus REST API endpoint.
        :type endpoint: str
        :param kwargs: as per :py:func:`requests.request`.
        :rtype: requests.Response
        """
        return self.http_request('put', endpoint, **kwargs)

    def http_delete(self, endpoint, **kwargs):
        """
        Performs a HTTP DELETE request on the given endpoint.

        :param endpoint: name of the Nexus REST API endpoint.
        :type endpoint: str
        :param kwargs: as per :py:func:`requests.request`.
        :rtype: requests.Response
        """
        return self.http_request('delete', endpoint, **kwargs)
