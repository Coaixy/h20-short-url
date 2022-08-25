# -*- coding: utf-8 -*-
# Author: XiaoXinYo

import os
import pymysql
import re
import time

class DataBase:
    def __init__(self):
        '''
        config = {
            'host': '127.0.0.1',
            'port': 3306,
            'username': 'root',
            'password': 'root',
            'database_name': 'db',
            'prefix': 'h2o_short_url_'
        }
        self.prefix = config.get('prefix')
        self.connect = pymysql.connect(host=config.get('host'), port=config.get('port'), user=config.get('username'), passwd=config.get('password'), db=config.get('database_name'))
        '''
        self.prefix = os.environ.get('prefix')
        self.connect = pymysql.connect(host=os.environ.get('host'), port=int(os.environ.get('port')), user=os.environ.get('username'), passwd=os.environ.get('password'), db=os.environ.get('database_name'))
        self.cursor = self.connect.cursor(pymysql.cursors.DictCursor)

    def __del__(self):
        self.cursor.close()
        self.connect.close()
    
    def existence_table(self, name):
        sql = 'show tables'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = re.findall('(\'.*?\')', str(data))
        data = [re.sub("'", '', data_count) for data_count in data]
        return f'{self.prefix}{name}' in data

    def create_core_table(self):
        sql = f'''
            CREATE TABLE `{self.prefix}core` (
                `key_d` varchar(255) NOT NULL,
                `value_d` varchar(255) DEFAULT NULL,
                PRIMARY KEY (`key_d`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        self.cursor.execute(sql)
        sql = f'insert into `{self.prefix}core` VALUES ("title", "氧化氢短网址");'
        self.cursor.execute(sql)
        self.connect.commit()
        sql = f'insert into `{self.prefix}core` VALUES ("keyword", "氧化氢短网址");'
        self.cursor.execute(sql)
        self.connect.commit()
        sql = f'insert into `{self.prefix}core` VALUES ("description", "一切是那么的简约高效.");'
        self.cursor.execute(sql)
        self.connect.commit()
        sql = f'insert into `{self.prefix}core` VALUES ("domain", "");'
        self.cursor.execute(sql)
        self.connect.commit()

    def create_url_table(self):
        sql = f'''
            CREATE TABLE `{self.prefix}url` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `type_d` varchar(255) DEFAULT NULL,
                `domain` varchar(255) DEFAULT NULL,
                `long_url` varchar(255) DEFAULT NULL,
                `signature` varchar(255) DEFAULT NULL,
                `valid_time` int(10) DEFAULT NULL,
                `count` bigint(255) DEFAULT NULL,
                `timestmap` int(10) DEFAULT NULL,
                PRIMARY KEY (`id`) USING BTREE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''
        self.cursor.execute(sql)

    def insert(self, type_d, domain, long_url, valid_time):
        sql = f'''
            insert into {self.prefix}url (type_d, domain, long_url, valid_time, count, timestmap) 
                    VALUES ("{type_d}", "{domain}", "{long_url}", {valid_time}, 0, {int(time.time())})
        '''
        self.cursor.execute(sql)
        id_d = self.connect.insert_id()
        self.connect.commit()
        return id_d
    
    def update(self, id_d, signature):
        sql = f'update {self.prefix}url set signature = "{signature}" where id = {id_d}'
        self.cursor.execute(sql)
        self.connect.commit()
    
    def add_count(self, domain, signature):
        sql = f'update {self.prefix}url set count = count + 1 where domain = "{domain}" and signature = "{signature}"'
        self.cursor.execute(sql)
        self.connect.commit()
    
    def query_website_information(self):
        sql = f'select * from {self.prefix}core where key_d = "title" or key_d = "keyword" or key_d = "description" limit 3'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        information = {}
        for data_count in data:
            information[data_count.get('key_d')] = data_count.get('value_d')
        return information

    def query_domain(self):
        sql = f'select * from {self.prefix}core where key_d = "domain" limit 1'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = data[0].get('value_d')
        data = data.split(',')
        return data

    def query_by_long_url(self, domain, long_url):
        sql = f'select * from {self.prefix}url where domain = "{domain}" and long_url = "{long_url}" limit 1'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data[0]
        return False

    def query_by_signature(self, domain, signature):
        sql = f'select * from {self.prefix}url where domain = "{domain}" and signature = "{signature}" limit 1'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if data:
            return data[0]
        return False