from django.conf import settings
import psycopg2
import csv
from django.db import connections


def GeoCode(conn):
    if conn:
        conn.set_isolation_level(0)
        cur = conn.cursor()
        with open('/home/shalini/csv/shalini.CSV') as f:
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

def GeoNom(conn):
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

def Topic(conn):
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

def Characteristics(conn):
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

def GeoProfile(conn):
    if conn:
        conn.set_isolation_level(0)
        cur = conn.cursor()
        with open('/home/shalini/csv/shalini.CSV') as f:
            reader= csv.reader(f)
            tableName = 'Geo_Profile'
            cur.execute("CREATE TABLE IF NOT EXISTS %s();"  % (tableName))
            for idx, val in enumerate(reader):
                if idx == 0:
                    # for column in val:
                    #     pass
                    query = "ALTER TABLE %s ADD COLUMN %s text REFERENCES Geo_Code (%s), ADD COLUMN %s text REFERENCES Geo_Nom (%s), ADD COLUMN %s text REFERENCES Topic (%s), ADD COLUMN %s text REFERENCES Characteristic (%s);"
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
                        print e.pgerror
                        pass
                else:
                    # val = [str(x) for x in val]
                    # print val
                    # val.insert(0, tableName)
                    # val = tuple(val)
                    # query = "INSERT INTO %s VALUES ('%s')" % (val[0])
                    # try:
                    #     cur.execute(query)
                    # except psycopg2.Error as e:
                    #     print e.pgerror
                    #     pass
    else:
        print "Sorry Buddy, No database connection"

if __name__ == '__main__':
    # try:
    #     conn=psycopg2.connect("dbname='shalini' user='root' password='shalini'")
    # except:
        conn = None
    try:
        conn=psycopg2.connect("dbname='ca_census' user='%s' password='%s' host='%s' port='%s'" % ( 
        settings.US_CENSUS_DB['USER'], settings.US_CENSUS_DB['PASSWORD'], settings.US_CENSUS_DB['HOST'],
        settings.US_CENSUS_DB['PORT']))
    except psycopg2.Error as e:
        conn = None
    GeoCode(conn)
    Topic(conn)
    Characteristics(conn)

