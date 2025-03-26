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

import ast
import json
import logging
import unittest

from sc_config import ConfigUtils
from sc_utilities import log_init

from sc_employee_synchronizer import PROJECT_NAME
from sc_employee_synchronizer.sync.employee_sync import EmployeeSynchronizer


class EmployeeSynchronizerTestCase(unittest.TestCase):

    def setUp(self):
        project_name = PROJECT_NAME
        ConfigUtils.clear(project_name)
        self._config = ConfigUtils.get_config(project_name)
        self._sync = EmployeeSynchronizer(config=self._config)
        self._json_filename = self._config.get("import.json.filename")
        self._log_filename = self._config.get("import.log.filename")
        self._log_marker = self._config.get("import.log.marker")

    def test_add_user_from_file(self):
        with open(self._json_filename, 'r', encoding='utf-8') as fp:
            employee_json = json.load(fp)
            self._sync._add_all_employee_to_db(employee_json)

    def test_read_from_log_file(self):
        try:
            all_employee_data = list()
            with open(self._log_filename, 'r', encoding='utf-8') as file:
                # 逐行读取文件内容
                for line_num, line in enumerate(file, 1):
                    # 移除行尾的换行符
                    processed_line = line.strip()
                    index = processed_line.find(self._log_marker)
                    if index >= 0:
                        logging.getLogger(__name__).info(f"Found marker at line {line_num}")
                        content = processed_line[index + len(self._log_marker):]
                        # 解析为 Python 字典（或列表）
                        data = ast.literal_eval(content)
                        all_employee_data.extend(data)
            self._sync._add_all_employee_to_db(all_employee_data)
        except Exception as e:
            logging.getLogger(__name__).error("failed to read content from file. cause: %s", e)


if __name__ == '__main__':
    log_init()
    unittest.main()
