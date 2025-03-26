import json
import logging
import re
from collections import defaultdict
from enum import Enum

import pymysql
from sc_config import ConfigManager
from pymysql import MySQLError
from sc_utilities import log_init

from sc_employee_synchronizer.db.common_db_module import CommonDBModule

log_init()


class FieldRelation(Enum):
    CHILD_FIELD = 0
    ONE_TO_ONE = 1
    ASSOCIATION_TABLE = 2  # 关联表类型


class FieldInfo:
    def __init__(self):
        self.types = set()
        self.max_length = 0
        self.nullable = True  # 默认允许NULL
        self.is_datetime = False
        self.is_primary = False  # 新增主键标识
        self.auto_increment = False  # 是否自增
        self.relation: FieldRelation = FieldRelation.CHILD_FIELD

    def add_value(self, value):
        if value is None:
            if not self.is_primary:  # 主键不允许为空
                self.nullable = True
            return
        self.types.add(type(value))
        if isinstance(value, str):
            if re.match(r'^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(\.\d+)?$', value):
                self.is_datetime = True
            self.max_length = max(self.max_length, len(value))
        elif isinstance(value, (int, float, bool)):
            pass

    @staticmethod
    def round_up_to_power_of_two(n):
        """计算最接近且不小于n的2次方数"""
        if n <= 0:
            return 1
        n -= 1
        n |= n >> 1
        n |= n >> 2
        n |= n >> 4
        n |= n >> 8
        n |= n >> 16
        n += 1
        return n
    def get_mysql_type(self):
        if self.is_datetime:
            return 'DATETIME'
        if str in self.types:
            # 自动计算最接近的2次方长度
            rounded_length = self.round_up_to_power_of_two(self.max_length)
            return 'TEXT' if rounded_length > 8192 else f'VARCHAR({rounded_length})'
        if bool in self.types:
            return 'TINYINT(1)'
        if int in self.types:
            if self.auto_increment:
                return 'BIGINT AUTO_INCREMENT'
            return 'INT'
        if float in self.types:
            return 'DOUBLE'
        return 'VARCHAR(64)'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (f"FieldInfo(types={self.types}, "
                f"max_length={self.max_length}, "
                f"nullable={self.nullable}, "
                f"is_datetime={self.is_datetime}, "
                f"is_primary={self.is_primary}, "
                f"relation={self.relation})")


class Json2DB:

    def __init__(self, *, config: ConfigManager):
        self._config = config
        self._db_module = CommonDBModule(config=config)
        self._root_table_name = self._config.get("import.db.root_table_name")

    # 驼峰转下划线函数
    @staticmethod
    def camel_to_snake(name):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    def process_object(self, obj, current_table, parent_table, schema):
        if current_table not in schema:
            schema[current_table] = defaultdict(FieldInfo)
            schema['_meta'][current_table] = {
                'parent': parent_table,
                'associations': defaultdict(list)  # 存储关联关系
            }

        fields = schema[current_table]
        meta = schema['_meta'][current_table]

        for key in list(obj.keys()):
            value = obj[key]
            # 特殊处理id字段
            if key == 'id':
                fields[key].is_primary = True
                fields[key].nullable = False  # 主键强制NOT NULL

            if isinstance(value, dict):
                child_table = f"{current_table}_{key}"
                self.process_object(value, child_table, current_table, schema)
                fields[key].relation = FieldRelation.ONE_TO_ONE
            elif isinstance(value, list):
                has_objects = any(isinstance(item, dict) for item in value)
                if has_objects:
                    # 创建子表
                    child_table = f"{current_table}_{key}"
                    # 创建关联表
                    assoc_table = f"{current_table}_{key}_assoc"

                    # 在元数据中记录关联关系
                    schema['_meta'][current_table]['associations'][key] = {
                        'child_table': child_table,
                        'assoc_table': assoc_table
                    }

                    # 初始化关联表结构
                    if assoc_table not in schema:
                        schema[assoc_table] = defaultdict(FieldInfo)
                        schema['_meta'][assoc_table] = {
                            'parent': current_table,
                            'relation_type': FieldRelation.ASSOCIATION_TABLE
                        }
                        # 添加主键
                        schema[assoc_table]["id"] = FieldInfo()
                        schema[assoc_table]["id"].types.add(int)
                        schema[assoc_table]["id"].is_primary = True
                        schema[assoc_table]["id"].auto_increment = True
                        schema[assoc_table]["id"].nullable = False
                        # 添加主表外键
                        schema[assoc_table][f"{current_table}_id"] = FieldInfo()
                        schema[assoc_table][f"{current_table}_id"].is_primary = False
                        # 添加子表外键
                        schema[assoc_table][f"{child_table}_id"] = FieldInfo()
                        schema[assoc_table][f"{child_table}_id"].is_primary = False

                    # 处理子表
                    for item in value:
                        if isinstance(item, dict):
                            self.process_object(item, child_table, current_table, schema)

                    # 从当前表删除原字段
                    if key in fields:
                        del fields[key]
                else:
                    if key in fields:
                        del fields[key]
            else:
                fields[key].add_value(value)

    def infer_mysql_types(self, schema):
        for table in schema:
            if table == '_meta':
                continue
            for field in schema[table].values():
                field.mysql_type = field.get_mysql_type()

    def generate_sql(self, schema):
        sql = []

        for table in schema['_meta']:
            create = []
            primary_keys = []
            # 转换当前表名为小写下划线格式
            table_name = Json2DB.camel_to_snake(table)
            # 处理关联表
            if schema['_meta'][table].get('relation_type') == FieldRelation.ASSOCIATION_TABLE:

                # 处理主键字段
                for field, info in schema[table].items():
                    if info.is_primary:
                        primary_keys.append(f"`{field}`")
                        create.append(f"`{field}` {info.mysql_type} NOT NULL")
                        create.append(f"PRIMARY KEY ({', '.join(primary_keys)})")

                # 主表外键字段
                parent_field = f"{schema['_meta'][table]['parent']}_id"
                parent_info = schema[table][parent_field]
                create.append(f"`{parent_field}` {parent_info.mysql_type} NOT NULL")

                # 子表外键字段
                child_field = next((k for k in schema[table].keys() if k.endswith('_id') and k != parent_field), None)
                if child_field:
                    child_info = schema[table][child_field]
                    create.append(f"`{child_field}` {child_info.mysql_type} NOT NULL")

                # 生成关联表SQL
                drop = f"DROP TABLE IF EXISTS `{table_name}`;"
                create_sql = f"CREATE TABLE `{table_name}` (\n  " + ",\n  ".join(create) + "\n);"
                sql.extend([drop, create_sql])
                continue

            for key in list(schema[table].keys()):
                info = schema[table][key]

            # 处理主键字段
            for field, info in schema[table].items():
                if info.is_primary:
                    primary_keys.append(f"`{field}`")
                    create.append(f"`{field}` {info.mysql_type} NOT NULL")

            # 添加联合主键约束
            if primary_keys:
                create.append(f"PRIMARY KEY ({', '.join(primary_keys)})")

            # 处理其他字段
            for field, info in schema[table].items():
                if info.is_primary:
                    continue
                null = 'NULL' if info.nullable else 'NOT NULL'
                create.append(f"`{field}` {info.mysql_type} {null}")

            # 生成完整SQL
            drop = f"DROP TABLE IF EXISTS `{table_name}`;"
            create_sql = f"CREATE TABLE `{table_name}` (\n  " + ",\n  ".join(create) + "\n);"
            sql.extend([drop, create_sql])
        return sql

    def insert_data(self, obj, current_table, conn, schema):
        cursor = None
        try:
            cursor = conn.cursor()
            if current_table not in schema['_meta']:
                return

            # 转换当前表名为小写下划线格式
            current_table_name = Json2DB.camel_to_snake(current_table)
            fields = schema[current_table]
            meta = schema['_meta'][current_table]
            data = {}

            for key in fields:
                if key in obj:
                    data[key] = obj[key]
                else:
                    data[key] = None

            columns = []
            values = []
            primary_key = None
            for col, val in data.items():
                if col not in fields:
                    continue
                field_info = fields[col]
                if field_info.is_primary:
                    primary_key = col
                if isinstance(val, bool):
                    val = '1' if val else '0'
                elif isinstance(val, str):
                    val = f"'{conn.escape_string(val)}'"
                elif val is None:
                    val = 'NULL'
                elif isinstance(val, (int, float)):
                    val = str(val)
                elif isinstance(val, dict):
                    val = str(val['id'])  # TODO 从子表中获取主键值
                else:
                    val = f"'{str(val)}'"
                columns.append(f"`{col}`")
                values.append(val)

            if columns:
                sql = (f"INSERT INTO `{current_table_name}` ({', '.join(columns)}) "
                       f"VALUES ({', '.join(values)}) "
                       f"ON DUPLICATE KEY UPDATE {primary_key}=VALUES({primary_key});")
                logging.info(sql)
                cursor.execute(sql)

            current_id = obj.get('id', cursor.lastrowid)
            for key, val in obj.items():
                if isinstance(val, dict):
                    child_table = f"{current_table}_{key}"
                    self.insert_data(val, child_table, conn, schema)
                elif isinstance(val, list):
                    for item in val:
                        if isinstance(item, dict):
                            assoc_table = f"{current_table}_{key}"
                            self.insert_data(item, assoc_table, conn, schema)

            # 处理关联关系
            associations = schema['_meta'][current_table].get('associations', {})
            for field, rel_info in associations.items():
                if field in obj:
                    child_table = rel_info['child_table']
                    assoc_table = rel_info['assoc_table']
                    # 转换当前表名为小写下划线格式
                    assoc_table_name = Json2DB.camel_to_snake(assoc_table)

                    for item in obj[field]:
                        # 插入子表数据
                        self.insert_data(item, child_table, conn, schema)
                        child_fields = schema[child_table]
                        for col in child_fields:
                            field_info = child_fields[col]
                            if field_info.is_primary:
                                primary_key = col
                                break
                        child_id = item.get(primary_key)

                        # 插入关联表数据
                        assoc_sql = (f"INSERT INTO `{assoc_table_name}` "
                                     f"(`{current_table}_id`, `{child_table}_id`) "
                                     f"VALUES ('{current_id}', '{child_id}') "
                                     f"ON DUPLICATE KEY UPDATE "
                                     f"{current_table}_id=VALUES({current_table}_id), "
                                     f"{child_table}_id=VALUES({child_table}_id);")
                        logging.info(assoc_sql)
                        cursor.execute(assoc_sql)
            conn.commit()
        except MySQLError as e:
            logging.error(f"Error: {e}")
            conn.rollback()
        except Exception as e:
            logging.exception(f"Unexpected error: {e}")  # 记录堆栈跟踪
            conn.rollback()
        finally:
            if cursor:
                cursor.close()

    def run(self, jsonData):
        # Build schema
        schema = defaultdict(dict)
        schema['_meta'] = {}
        current_table = self._root_table_name
        # 转换当前表名为小写下划线格式
        current_table = Json2DB.camel_to_snake(current_table)
        for record in jsonData:
            self.process_object(record, current_table, None, schema)
        self.infer_mysql_types(schema)
        logging.info(json.dumps(schema, indent=2, ensure_ascii=False, default=str))

        conn = None
        # Execute SQL
        try:
            # Load configurations
            db_config = self._config['db']
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()
            # Generate SQL
            sql_statements = self.generate_sql(schema)
            for stmt in sql_statements:
                logging.info(stmt)
                cursor.execute(stmt)
            conn.commit()
            cursor.close()

            # Insert data
            for record in jsonData:
                self.insert_data(record, current_table, conn, schema)
        except MySQLError as e:
            logging.error(f"Database error: {e}")
        finally:
            if conn:
                conn.close()
