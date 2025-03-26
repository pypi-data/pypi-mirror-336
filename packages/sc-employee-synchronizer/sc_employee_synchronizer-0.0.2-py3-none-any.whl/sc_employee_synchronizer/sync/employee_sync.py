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

import json
import logging
from datetime import datetime

from sc_config import ConfigManager

from sc_employee_synchronizer.api.request_api import RequestClient
from sc_employee_synchronizer.db.json2db import Json2DB
from sc_employee_synchronizer.exception.exceptions import *
from sc_employee_synchronizer.utils.conversion_utils import str2bool


class EmployeeSynchronizer(RequestClient):
    API_KEY_GRANT_TYPE = "grant_type"
    GRANT_TYPE_CLIENT_CREDENTIALS = "client_credentials"
    API_KEY_CLIENT_ID = "client_id"
    API_KEY_CLIENT_SECRET = "client_secret"
    API_KEY_ACCESS_TOKEN = "access_token"

    RESULT_KEY_CONTENT = "content"
    RESULT_KEY_NAME = "name"
    RESULT_KEY_USER_ID = "username"
    RESULT_KEY_ID_CARD_NO = "identityCardNo"
    RESULT_KEY_DEPARTMENT = "department"
    RESULT_KEY_DEPARTMENT_NAME = "name"
    RESULT_KEY_PHONE = "cellphoneNumber"
    RESULT_KEY_POSITION = "position"
    RESULT_KEY_ENABLED = "enabled"
    RESULT_KEY_GENDER = "gende"
    RESULT_KEY_CATEGORY = "category"
    RESULT_KEY_CREATE_TIME = "joinDate"
    RESULT_KEY_MODIFY_TIME = "ehrModifyDate"
    PAGE_SIZE = 50

    def __init__(self, *, config: ConfigManager):
        self._config = config
        self._start_time = datetime.now()
        self._end_time = datetime.now()
        self._employee_list = list()
        self._partner_employee_list = list()
        self._failed_db_list = list()
        self._failed_gitlab_list = list()
        self._read_config(config=config)
        super(EmployeeSynchronizer, self).__init__(
            url=EmployeeSynchronizer._get_real_url(self._server, self._port),
        )

    def _read_config(self, *, config: ConfigManager):
        self._server = config.get("synchronizer.server")
        self._port = config.get("synchronizer.port")
        self._token_url = config.get("synchronizer.token_url")
        self._grant_type = config.get("synchronizer.grant_type")
        self._get_yesterday_added_user_url = config.get("synchronizer.get_yesterday_added_user_url")
        self._get_all_partner_url = config.get("synchronizer.get_all_partner_url")
        self._get_all_user_url = config.get("synchronizer.get_all_user_url")
        self._client_id = config.get("synchronizer.client_id")
        self._client_secret = config.get("synchronizer.client_secret")
        self._only_include_enabled = config.get("synchronizer.only_include_enabled")
        self._all = config.get("synchronizer.import_all_users")
        self._import_to_db = config.get("import.db.enabled")

    @staticmethod
    def _get_real_url(server, port):
        base_url = "http://{0}:{1}".format(server, port)
        return base_url

    def _get_access_token(self):
        params = {
            EmployeeSynchronizer.API_KEY_GRANT_TYPE: EmployeeSynchronizer.GRANT_TYPE_CLIENT_CREDENTIALS,
            EmployeeSynchronizer.API_KEY_CLIENT_ID: self._client_id,
            EmployeeSynchronizer.API_KEY_CLIENT_SECRET: self._client_secret,
        }
        return self.http_request('get', self._token_url, params=params)

    def _get_yesterday_added_users(self, access_token):
        params = {
            EmployeeSynchronizer.API_KEY_ACCESS_TOKEN: access_token,
        }
        return self.http_request('get', self._get_yesterday_added_user_url, params=params)

    def _get_all_users(self, access_token, page_data_params):
        params = {
            EmployeeSynchronizer.API_KEY_ACCESS_TOKEN: access_token,
        }
        return self.http_request(
            'post',
            self._get_all_user_url,
            params=params,
            data=json.dumps(page_data_params),
            headers={'Content-type': 'application/json;charset=UTF-8'},
        )

    # 获取人员的全部信息
    def _get_employee_users(self, access_token):
        page_size = EmployeeSynchronizer.PAGE_SIZE
        page_no = 1

        data = {
            "username": "",
            "name": "",
            "organizationName": "",
            "pageNo": page_no,
            "pageSize": page_size,
        }
        if self._only_include_enabled:
            data["enabled"] = True

        all_employee_data = list()
        retry_count = 3
        while True:
            logging.getLogger(__name__).info(f"get page {page_no} data")
            resp_data = self._get_all_users(access_token=access_token, page_data_params=data)
            if resp_data.status_code != 200:
                msg = "failed to get new users' information, Error Code:{0}".format(resp_data.status_code)
                logging.getLogger(__name__).error(msg)
                retry_count = retry_count - 1
                if retry_count == 0:
                    # 三次失败，就换下一页
                    page_no += 1
                    data["pageNo"] = page_no
                    retry_count = 3
                    continue
                else:
                    # 重试三次
                    continue
            response_data = resp_data.json()
            if EmployeeSynchronizer.RESULT_KEY_CONTENT not in response_data:
                logging.getLogger(__name__).error(f"illegal response data")
                break
            content = response_data[EmployeeSynchronizer.RESULT_KEY_CONTENT]
            logging.getLogger(__name__).info(f"result content: {content}")
            if content is None or len(content) == 0:
                logging.getLogger(__name__).info(f"already fetched the last page")
                break
            all_employee_data.extend(content)
            page_no += 1
            data["pageNo"] = page_no

        return all_employee_data

    def _add_all_employee_to_db(self, all_employee_list):
        logging.getLogger(__name__).info("importing all employee users to database")
        json2db = Json2DB(config=self._config)
        json2db.run(jsonData=all_employee_list)

    def run(self):
        self._start_time = datetime.now()
        response = self._get_access_token()
        code = response.status_code
        if code != 200:
            raise HttpClientAPIError("failed to get access token, Error Code:{0}".format(code))
        ret_json = response.json()
        if EmployeeSynchronizer.API_KEY_ACCESS_TOKEN not in ret_json:
            raise HttpClientAPIError("access token not found in response")
        access_token = response.json().get(EmployeeSynchronizer.API_KEY_ACCESS_TOKEN)
        logging.getLogger(__name__).info("adding all employee users from it dev platform")
        employee_list = []
        if self._all:
            employee_list.extend(self._get_employee_users(access_token))
        else:
            resp_data = self._get_yesterday_added_users(access_token)
            if resp_data.status_code != 200:
                msg = "failed to get new users' information, Error Code:{0}".format(resp_data.status_code)
                logging.getLogger(__name__).error(msg)
                return
            content = resp_data.json()
            logging.getLogger(__name__).info(f"result content: {content}")
            if content is None or len(content) == 0:
                logging.getLogger(__name__).error(f"no newly added employee")
                return
            employee_list.extend(content)

        if len(employee_list) == 0:
            logging.getLogger(__name__).info("user list is empty")
            return

        try:
            today = self._start_time.strftime("%Y%m%d")
            output_filename = f'data-{today}'
            if not self._all:
                output_filename += '_inc'
            output_filename += '.json'
            with open(output_filename, 'w', encoding='utf-8') as f:
                logging.getLogger(__name__).info(f"write result data to file")
                json.dump(employee_list, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.getLogger(__name__).error("failed to write employee json to file. cause: %s", e)

        if self._import_to_db:
            self._add_all_employee_to_db(employee_list)
