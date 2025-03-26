# -*- coding: utf-8 -*-

import sqlite3
from pendulum import DateTime, Date

from ..dbal.platforms import SQLitePlatform
from .connector import Connector
from ..utils.qmarker import qmark, denullify
from ..utils.helpers import serialize


class Record(dict):
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item)

    def serialize(self):
        return serialize(self)


class SQLiteConnector(Connector):
    def _do_connect(self, config):
        config = dict(config.items())
        config["check_same_thread"] = False
        config["detect_types"] = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES

        return sqlite3.connect(**config)

    def get_default_config(self):
        return {}

    def get_dbal_platform(self):
        return SQLitePlatform()

    def _register_pendulum_adapters(self):
        """
        Register Pendulum adapters for SQLite.
        """
        from sqlite3 import register_adapter

        register_adapter(DateTime, lambda val: val.isoformat(" "))
        register_adapter(Date, lambda val: val.isoformat())

    def get_api(self):
        return sqlite3

    @property
    def isolation_level(self):
        return self._connection.isolation_level

    @isolation_level.setter
    def isolation_level(self, value):
        self._connection.isolation_level = value

    def is_version_aware(self):
        return False

    def get_server_version(self):
        sql = "select sqlite_version() AS sqlite_version"

        rows = self._connection.execute(sql).fetchall()
        version = rows[0]["sqlite_version"]

        return tuple(version.split(".")[:3] + [""])
