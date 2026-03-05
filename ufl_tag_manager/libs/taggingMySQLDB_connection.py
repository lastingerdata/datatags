# ufl_tag_manager/libs/taggingMySQLDB_connection.py

import mysql.connector
import env_config


class LocalDBConnection:
    def connect(self):
        cfg = env_config.get_mysql_config()
        return mysql.connector.connect(
            host=cfg["host"],
            user=cfg["user"],
            password=cfg["password"],
            database=cfg["database"],
            port=cfg["port"],
        )