import mysql.connector
import env_config

class LocalDBConnection:

    def connect(self):
        cfg = env_config.get_mysql_config()
        conn = mysql.connector.connect(**cfg)
        
        return conn