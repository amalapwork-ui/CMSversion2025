# DbConnection/ConnectionDb.py
import mysql.connector
import configparser
import os
from mysql.connector import errorcode
from Exceptions.Errors import DBError

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db_config.ini")

class ConnectionDb:
    _instance = None

    def __init__(self):
        # private: load config only once
        config = configparser.ConfigParser()
        if not os.path.exists(CONFIG_PATH):
            raise FileNotFoundError(f"db_config.ini not found at {CONFIG_PATH}")
        config.read(CONFIG_PATH)
        if 'mysql' not in config:
            raise KeyError("Section 'mysql' not found in db_config.ini")
        mysql_cfg = config['mysql']
        self._cfg = {
            'host': mysql_cfg.get('host', '127.0.0.1'),
            'port': mysql_cfg.getint('port', 3306),
            'user': mysql_cfg.get('user'),
            'password': mysql_cfg.get('password'),
            'database': mysql_cfg.get('database'),
            'autocommit': False,
        }

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ConnectionDb()
        return cls._instance

    def get_connection(self):
        """Return a new connection. Caller must close it."""
        try:
            conn = mysql.connector.connect(**self._cfg)
            return conn
        except mysql.connector.Error as err:
            # Helpful error messages
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise ConnectionError("Invalid DB credentials") from err
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise ConnectionError("Database does not exist") from err
            else:
                raise

    # convenience helper for simple queries (select)
    # def fetch_all(self, query, params=None):
    #     conn = self.get_connection()
    #     cur = conn.cursor(dictionary=True)
    #     try:
    #         cur.execute(query, params or ())
    #         rows = cur.fetchall()
    #         return rows
    #     finally:
    #         cur.close()
    #         conn.close()
    def fetch_all(self, query, params=None):
        conn = self.get_connection()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute(query, params or ())
            rows = cur.fetchall()
            return rows
        except Exception as e:
            # wrap as DBError preserving original
            raise DBError(str(e))
        finally:
            cur.close()
            conn.close()

    def execute(self, query, params=None, commit=True):
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            cur.execute(query, params or ())
            if commit:
                conn.commit()
            return cur.lastrowid
        except Exception as e:
            conn.rollback()
            raise DBError(str(e))
        finally:
            cur.close()
            conn.close()

    # convenience helper for insert/update/delete
    # def execute(self, query, params=None, commit=True):
    #     conn = self.get_connection()
    #     cur = conn.cursor()
    #     try:
    #         cur.execute(query, params or ())
    #         if commit:
    #             conn.commit()
    #         return cur.lastrowid
    #     except Exception:
    #         conn.rollback()
    #         raise
    #     finally:
    #         cur.close()
    #         conn.close()
