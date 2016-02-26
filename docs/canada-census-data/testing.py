import os
from os import path

import psycopg2
import csv

# from django.db import connections
from django.conf import settings

def GeoCode(conn, files):
for file in files:
    if conn:
        conn.set_isolation_level(0)
        cur = conn.cursor()
        with open(file) as f:
            reader= csv.reader(f)
            tableName = 'Geo_Prov'
            cur.execute("CREATE TABLE IF NOT EXISTS %s();"  % (tableName))
            for idx, val in enumerate(reader):
                if idx == 0:
                    # for column in val:
                    #     pass
                    print val
                    query = "ALTER TABLE %s ADD COLUMN %s BIGSERIAL, ADD %s text UNIQUE, ADD %s text UNIQUE;" % (tableName, 'geo_id', val[0], val[1])
                    print query
                    try:
                        cur.execute(query)
                    except psycopg2.Error as e:
                        print e.pgerror
                        pass
                else:
                    val = [str(x) for x in val]
                    print val
                    val = val[:2]
                    val.insert(0, tableName)
                    print tuple(val)
                    query = "INSERT INTO %s (Geo_Code, Prov_Name) VALUES ('%s', '%s')" % tuple(val)
                    try:
                        cur.execute(query)
                    except psycopg2.Error as e:
                        print e.pgerror
                        pass
    else:
        print "Sorry Buddy, No database connection"

def GeoNom(conn, files):
    for file in files:
        if conn:
            conn.set_isolation_level(0)
            cur = conn.cursor()
            with open('/home/shalini/csv/shalini.CSV') as f:
                reader= csv.reader(f)
                tableName = 'Geo_Nom'
                cur.execute("CREATE TABLE IF NOT EXISTS %s();"  % (tableName))
                for idx, val in enumerate(reader):
                    if idx == 0:
                        # for column in val:
                        #     pass
                        query = "ALTER TABLE %s ADD COLUMN %s BIGSERIAL PRIMARY KEY, ADD %s text UNIQUE;" % (tableName, 'nom_id', val[2])
                        print query
                        try:
                            cur.execute(query)
                        except psycopg2.Error as e:
                            print e.pgerror
                            pass
                    else:
                        val = [str(x) for x in val]
                        val = val[2:8]
                        val.insert(0, tableName)
                        print tuple(val)
                        query = "INSERT INTO %s (Topic) VALUES ('%s')" % tuple(val)
                        try:
                            cur.execute(query)
                        except psycopg2.Error as e:
                            print e.pgerror
                            pass
        else:
            print "Sorry Buddy, No database connection"

def Topic(conn, files):
    for file in files:
        if conn:
            conn.set_isolation_level(0)
            cur = conn.cursor()
            with open('/home/shalini/csv/shalini.CSV') as f:
                reader= csv.reader(f)
                tableName = 'Characteristic'
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

def Characteristics(conn, files):
    for file in files:
        if conn:
            conn.set_isolation_level(0)
            cur = conn.cursor()
            with open('/home/shalini/csv/shalini.CSV') as f:
                reader= csv.reader(f)
                tableName = 'Characteristic'
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

def GeoProfile(conn, files):
    for file in files:
        if conn:
            conn.set_isolation_level(0)
            cur = conn.cursor()
            with open(file) as f:
                reader= csv.reader(f)
                tableName = 'Geo_Profile'
                cur.execute("CREATE TABLE IF NOT EXISTS %s();"  % (tableName))
                for idx, val in enumerate(reader):
                    if idx == 0:
                        # for column in val:
                        #     pass
                        query = "ALTER TABLE %s ADD COLUMN %s text REFERENCES Geo_Prov (%s), ADD COLUMN %s text REFERENCES Geo_Nom (%s), ADD COLUMN %s text REFERENCES Topic (%s), ADD COLUMN %s text REFERENCES Characteristic (%s);"
                                 % (tableName, 'geo_id', 'geo_id', 'nom_id', 'nom_id', 'topic_id', 'topic_id', 'char_id', 'char_id')
                        print query
                        try:
                            cur.execute(query)
                        except psycopg2.Error as e:
                            print e.pgerror
                            pass
                        query = "ALTER TABLE %s ADD COLUMN %s integer, ADD COLUMN %s integer, ADD COLUMN %s integer, ADD COLUMN %s integer;"
                                 % (tableName, val[5], val[6], val[8], val[10])
                        print query
                        try:
                            cur.execute(query)
                        except psycopg2.Error as e:
                            print e.pgerror0
                            pass
                    else:
                        val = [str(x) for x in val]
                        query = "INSERT INTO %s values (%s, %s, %s, %s, %s, %s, %s, %s)  % "
                        (tableName, func1(cur, val[0], val[1]), func2(cur, val[2]), func3(cur, val[3]), func4(cur, val[4]), val[5], val[6], val[8], val[10])
                        try:
                            cur.execute(query)
                        except psycopg2.Error as e:
                            print e.pgerror
                            pass
        else:
            print "Sorry Buddy, No database connection"

def func1(val0, val1):
    query = "SELECT geo_id from Geo_Prov WHERE Geo_Code=str(val0);"
    cur.execute(query)
    result = cur.fetchone()
    result = str(result[0]).strip("L")
    return result

def func2(val2):
    query = "SELECT nom_id from Geo_Nom WHERE Geo_Nom=str(val2);"
    cur.execute(query)
    result = cur.fetchone()
    result = str(result[0]).strip("L")
    return result

def func3(val3):
    query = "SELECT topic_id from Topic WHERE Topic=str(val3);"
    cur.execute(query)
    cur.execute(query)
    result = cur.fetchone()
    result = str(result[0]).strip("L")
    return result

def func4(val4):
    query = "SELECT char_id from Characteristic WHERE Characteristic=str(val4);"
    cur.execute(query)
    cur.execute(query)
    result = cur.fetchone()
    result = str(result[0]).strip("L")
    return result




if __name__ == '__main__':
        # try:
        # conn=psycopg2.connect("dbname='shalini' user='root' password='shalini'")
        # except:
        # conn = None
    try:
        conn=psycopg2.connect("dbname='us_census' user='%s' password='%s' host='%s' port='%s'" % ( 
        settings.US_CENSUS_DB['USER'], settings.US_CENSUS_DB['PASSWORD'], settings.US_CENSUS_DB['HOST'],
        settings.US_CENSUS_DB['PORT']))
    except psycopg2.Error as e:
        conn = None
    listfile = []
    directory_path = '/home/shalini/csv/new1/'
    for dirpath,_,filenames in os.walk(directory_path):
        for f in filenames:
        list_files = os.path.abspath(os.path.join(dirpath, f))
        listfile.append(list_files)
    files = [x for x in listfile if 'Metadata' not in x]
    GeoCode(conn, files)
    Topic(conn, files)
    Characteristics(conn, files)

