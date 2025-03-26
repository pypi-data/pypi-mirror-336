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


from sc_config import ConfigManager
from mysqlhelper import MySQLHelper


class CommonDBModule:
    """
    数据库操作模块
    """

    def __init__(self, *, config: ConfigManager):
        self._config = config
        # 数据库相关配置
        self._host = self._config.get("db.host")
        self._port = self._config.get("db.port")
        self._user = self._config.get("db.user")
        self._password = self._config.get("db.password")
        self._database = self._config.get("db.database")
        # 初始化数据库对接
        self._helper = MySQLHelper(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database,
        )

    def select_one(self, *, sql='', param=()):
        return self._helper.select_one(sql=sql, param=param)

    def select_all(self, *, sql='', param=()):
        return self._helper.select_all(sql=sql, param=param)

    def execute(self, *, sql='', param=(), auto_close=False):
        return self._helper.execute(sql=sql, param=param, auto_close=auto_close)
