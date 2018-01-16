#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import psycopg2

from .linggle import Linggle

LINGGLE_TABLE = os.environ.get('LINGGLE_TABLE', 'LINGGLE')
QUERY_CMD = "SELECT results FROM {} WHERE query=%s;".format(LINGGLE_TABLE)

settings = {
    'dbname': os.environ.get('PGDATABASE', 'linggle'),
    'host': os.environ.get('PGHOST', 'localhost'),
    'user': os.environ.get('PGUSER', 'linggle'),
    'password': os.environ.get('PGPASSWORD', ''),
    'port': int(os.environ.get('PGPORT', 5432))
}


class PostgresLinggle(Linggle):
    def __init__(self):
        self.conn = psycopg2.connect(**settings)

    def close(self):
        if hasattr(self, 'conn') and not self.conn.closed:
            self.conn.close()

    def query(self, cmd):
        with self.conn.cursor() as cursor:
            cursor.execute(QUERY_CMD, [cmd])
            res = cursor.fetchone()
            if res:
                return res[0]
        return []
