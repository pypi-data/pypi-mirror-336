# -*- coding: utf-8 -*-
import time
import sys
import mysql.connector
import logging

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
#log = logging.getLogger(__name__)	## 로그 설정
# 로거 설정
log = logging.getLogger(__name__)
log.debug("Logging Started... {}".format(__name__))

class DBMS():
    
    def __init__(self, config):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(**config)
            # dictionary=True을 이용하여 딕셔너리 형태로 보여줌
            self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        except mysql.connector.Error as e:
            print(e)
            sys.exit()

    def query(self, sql, args=None):
        self.cursor.execute(sql, args)
        return self.cursor

    def insert(self,sql,args=None):
        cursor = self.query(sql, args)
        id = cursor.lastrowid
        self.connection.commit()
        return id

    def insertmany(self,sql,args):
        self.cursor.executemany(sql, args)
        rowcount = self.cursor.rowcount
        self.connection.commit()
        return rowcount

    def update(self, sql, args=None):
        cursor = self.query(sql, args)
        rowcount = cursor.rowcount
        self.connection.commit()
        return rowcount

    def fetch(self, sql, args=None):
        """ execute query """    	
        rows = []
        cursor = self.query(sql, args)
        if cursor.with_rows:
            rows = cursor.fetchall()
        return rows

    def fetchone(self, sql, args=None):
        """ get one row """    	
        row = None
        cursor = self.query(sql, args)
        if cursor.with_rows:
            row = cursor.fetchone()
        return row
    
    def getsql(self):
        """ get sql statement """    	
        statement = self.cursor.statement
        return statement

    def __del__(self):
        #self.cursor.close()
        if self.connection != None:
            self.connection.close()
        pass


if __name__=="__main__":
    
    mysql3 = {
        'host': 'localhost',
        'user': 'root',
        'password': 'autoset',
        'database': 'test'
    }

    sql = 'select * from seller limit 10'

    db = DBMS(mysql3)
    rows = db.fetch(sql)	
    for row in rows:
        print('{} -- {}'.format(row, type(row)))


    