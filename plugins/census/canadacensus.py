import os
from os import path

import psycopg2
import csv

# from django.db import connections
from django.conf import settings

class CanadaCensus:

    def __init__(self):

        # try:
            # conn=psycopg2.connect("dbname='shalini' user='root' password='shalini'")
        # except:
            # conn = None
        try:
            self.conn=psycopg2.connect("dbname='us_census' user='%s' password='%s' host='%s' port='%s'" % (
            settings.US_CENSUS_DB['USER'], settings.US_CENSUS_DB['PASSWORD'], settings.US_CENSUS_DB['HOST'],
            settings.US_CENSUS_DB['PORT']))
        except psycopg2.Error as e:
            self.conn = None
        listfile = []
        directory_path = '/home/ec2-user/canada/'
        for dirpath,_,filenames in os.walk(directory_path):
            for f in filenames:
                list_files = os.path.abspath(os.path.join(dirpath, f))
                listfile.append(list_files)
        self.files = [x for x in listfile if 'Metadata' not in x]


    def GeoCode(self):
        for file in self.files:
            print "Going through %s file for Geo_Prov table" % (file)
            if self.conn:
                self.conn.set_isolation_level(0)
                cur = self.conn.cursor()
                with open(file) as f:
                    reader= csv.reader(f)
                    tableName = 'Geo_Prov'
                    cur.execute("DROP TABLE IF EXISTS %s;" % (tableName))
                    cur.execute("CREATE TABLE IF NOT EXISTS %s();"  % (tableName))
                    for idx, val in enumerate(reader):
                        if idx == 0:
                            # for column in val:
                            #     pass
                            print val
                            query = "ALTER TABLE %s ADD COLUMN %s BIGSERIAL PRIMARY KEY, ADD %s text UNIQUE, ADD %s text UNIQUE;" % (tableName, 'geo_id', val[0], val[1])
                            try:
                                cur.execute(query)
                            except psycopg2.Error as e:
                                print e.pgerror
                                pass
                        else:
                            val = [str(x) for x in val]
                            val = val[:2]
                            val.insert(0, tableName)
                            query = "INSERT INTO %s (Geo_Code, Prov_Name) VALUES ('%s', '%s')" % tuple(val)
                            try:
                                cur.execute(query)
                            except psycopg2.Error as e:
                                pass
            else:
                print "Sorry Buddy, No database connection"

    def GeoNom(self):
        for file in self.files:
            print "Going through %s file for Geo_Nom table" % (file)
            if self.conn:
                self.conn.set_isolation_level(0)
                cur = self.conn.cursor()
                with open(file) as f:
                    reader= csv.reader(f)
                    tableName = 'Geo_Nom'
                    cur.execute("DROP TABLE IF EXISTS %s;" % (tableName))
                    cur.execute("CREATE TABLE IF NOT EXISTS %s();"  % (tableName))
                    for idx, val in enumerate(reader):
                        if idx == 0:
                            # for column in val:
                            #     pass
                            query = "ALTER TABLE %s ADD COLUMN %s BIGSERIAL PRIMARY KEY, ADD %s text UNIQUE;" % (tableName, 'nom_id', val[2])
                            try:
                                cur.execute(query)
                            except psycopg2.Error as e:
                                print e.pgerror
                                pass
                        else:
                            val = [str(x) for x in val]
                            val = val[2:8]
                            val.insert(0, tableName)
                            print "val: {val}".format(val=tuple(val))
                            query = "INSERT INTO %s (Topic) VALUES ('%s')" % tuple(val)
                            try:
                                cur.execute(query)
                            except psycopg2.Error as e:
                                print e.pgerror
                                pass
            else:
                print "Sorry Buddy, No database connection"


    def Topic(self):
        for file in self.files:
            print "Going through %s file for Topic table" % (file)
            if self.conn:
                self.conn.set_isolation_level(0)
                cur = self.conn.cursor()
                with open(file) as f:
                    reader= csv.reader(f)
                    tableName = 'Topic'
                    cur.execute("DROP TABLE IF EXISTS %s;" % (tableName))
                    cur.execute("CREATE TABLE IF NOT EXISTS %s();"  % (tableName))
                    for idx, val in enumerate(reader):
                        if idx == 0:
                            # for column in val:
                            #     pass
                            query = "ALTER TABLE %s ADD COLUMN %s BIGSERIAL PRIMARY KEY,ADD %s text UNIQUE;" % (tableName, 'topic_id', val[2])
                            print query
                            try:
                                cur.execute(query)
                            except psycopg2.Error as e:
                                print e.pgerror
                                pass
                        else:
                            val = [str(x) for x in val]
                            val = val[3:7]
                            val.insert(0, tableName)
                            print tuple(val)
                            query = "INSERT INTO %s () VALUES ('%s')" % tuple(val)
                            try:
                                cur.execute(query)
                            except psycopg2.Error as e:
                                print e.pgerror
                                pass
            else:
                print "Sorry Buddy, No database connection"

    def Characteristics(self):
        for file in self.files:
            print "Going through %s file for Characteristic table" % (file)
            if self.conn:
                self.conn.set_isolation_level(0)
                cur = self.conn.cursor()
                with open(file) as f:
                    reader= csv.reader(f)
                    tableName = 'Characteristic'
                    cur.execute("DROP TABLE IF EXISTS %s;" % (tableName))
                    cur.execute("CREATE TABLE IF NOT EXISTS %s();"  % (tableName))
                    for idx, val in enumerate(reader):
                        if idx == 0:
                            # for column in val:
                            #     pass
                            query = "ALTER TABLE %s ADD COLUMN %s BIGSERIAL PRIMARY KEY, ADD %s text UNIQUE;" % (tableName, 'char_id', val[3])
                            print query
                            try:
                                cur.execute(query)
                            except psycopg2.Error as e:
                                print e.pgerror
                                pass
                        else:
                            val = [str(x) for x in val]
                            val = val[3:7]
                            val.insert(0, tableName)
                            print tuple(val)
                            query = "INSERT INTO %s (Characteristic) VALUES ('%s')" % tuple(val)
                            try:
                                cur.execute(query)
                            except psycopg2.Error as e:
                                print e.pgerror
                                pass
            else:
                print "Sorry Buddy, No database connection"

    def GeoProfile(self):
        for file in self.files:
            print "Going through %s file for Geo_Profile table" % (file)
            if self.conn:
                self.conn.set_isolation_level(0)
                cur = self.conn.cursor()
                with open(file) as f:
                    reader= csv.reader(f)
                    tableName = 'Geo_Profile'
                    cur.execute("DROP TABLE IF EXISTS %s;" % (tableName))
                    cur.execute("CREATE TABLE IF NOT EXISTS %s();"  % (tableName))
                    for idx, val in enumerate(reader):
                        if idx == 0:
                            # for column in val:
                            #     pass
                            query = "ALTER TABLE %s ADD COLUMN %s text REFERENCES Geo_Prov (%s), ADD COLUMN %s text REFERENCES Geo_Nom (%s), ADD COLUMN %s text REFERENCES Topic (%s), ADD COLUMN %s text REFERENCES Characteristic (%s);" % (tableName, 'geo_id', 'geo_id', 'nom_id', 'nom_id', 'topic_id', 'topic_id', 'char_id', 'char_id')
                            try:
                                cur.execute(query)
                            except psycopg2.Error as e:
                                print e.pgerror
                                pass
                            query = "ALTER TABLE %s ADD COLUMN %s integer, ADD COLUMN %s integer, ADD COLUMN %s integer, ADD COLUMN %s integer;" % (tableName, val[5], val[6], val[8], val[10])
                            try:
                                cur.execute(query)
                            except psycopg2.Error as e:
                                print e.pgerror0
                                pass
                        else:
                            val = [str(x) for x in val]
                            query = "INSERT INTO %s values (%s, %s, %s, %s, %s, %s, %s, %s)" % (tableName, func1(val[0], val[1]), func2(val[2]), func3(val[3]), func4(val[4]), val[5], val[6], val[8], val[10])
                            try:
                                cur.execute(query)
                            except psycopg2.Error as e:
                                pass
            else:
                print "Sorry Buddy, No database connection"

    def func1(self, val0, val1):
        query = "SELECT geo_id from Geo_Prov WHERE Geo_Code=str(val0);"
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        result = str(result[0]).strip("L")
        return result

    def func2(self, val2):
        query = "SELECT nom_id from Geo_Nom WHERE Geo_Nom=str(val2);"
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        result = str(result[0]).strip("L")
        return result

    def func3(self, val3):
        query = "SELECT topic_id from Topic WHERE Topic=str(val3);"
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        result = str(result[0]).strip("L")
        return result

    def func4(self, val4):
        query = "SELECT char_id from Characteristic WHERE Characteristic=str(val4);"
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        result = str(result[0]).strip("L")
        return result



