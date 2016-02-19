from django.conf import settings
import psycopg2
import csv


def GeoCode(conn):
    if conn:
        conn.set_isolation_level(0)
        cur = conn.cursor()
        with open('/home/shalini/csv/shalini.CSV') as f:
            reader= csv.reader(f)
            tableName = 'Geo_Code'
            cur.execute("CREATE TABLE IF NOT EXISTS %s();"  % (tableName))
            for idx, val in enumerate(reader):
                if idx == 0:
                    # for column in val:
                    #     pass
                    query = "ALTER TABLE %s ADD COLUMN %s SERIAL, ADD %s text UNIQUE, ADD %s text UNIQUE;" % (tableName, 'geo_id', val[0], val[1])
                    print query
                    try:
                        cur.execute(query)
                    except psycopg2.Error as e:
                        print e.pgerror
                        pass
                else:
                    val = [str(x) for x in val]
                    val = val[:2]
                    val.insert(0, tableName)
                    print tuple(val)
                    query = "INSERT INTO %s VALUES ('%s', '%s')" % tuple(val)
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
                    query = "ALTER TABLE %s ADD COLUMN %s SERIAL PRIMARY KEY, ADD %s text UNIQUE;" % (tableName, 'nom_id', val[2])
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
                    query = "INSERT INTO %s VALUES ('%s')" % tuple(val)
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
                    query = "ALTER TABLE %s AADD COLUMN %s SERIAL PRIMARY KEY,ADD %s text UNIQUE;" % (tableName, 'topic_id', val[2])
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
                    query = "INSERT INTO %s VALUES ('%s')" % tuple(val)
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
                    query = "ALTER TABLE %s ADD COLUMN %s SERIAL PRIMARY KEY, ADD %s text UNIQUE;" % (tableName, 'char_id', val[3])
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
                    query = "INSERT INTO %s VALUES ('%s')" % tuple(val)
                    try:
                        cur.execute(query)
                    except psycopg2.Error as e:
                        print e.pgerror
                        pass
    else:
        print "Sorry Buddy, No database connection"

# def GeoProfile(conn):
#     if conn:
#         conn.set_isolation_level(0)
#         cur = conn.cursor()
#         with open('/home/shalini/csv/shalini.CSV') as f:
#             reader= csv.reader(f)
#             tableName = 'Geo_Profile'
#             cur.execute("CREATE TABLE IF NOT EXISTS %s();"  % (tableName))
#             for idx, val in enumerate(reader):
#                 if idx == 0:
#                     # for column in val:
#                     #     pass
#                     query = "ALTER TABLE %s ADD COLUMN %s text REFERENCES GeoId (%s), ADD COLUMN %s text REFERENCES GeoId (%s);"
#                              % (tableName, 'geoid', 'geoid', 'topic', 'topic')
#                     print query
#                     try:
#                         cur.execute(query)
#                     except psycopg2.Error as e:
#                         print e.pgerror
#                         pass
#                 else:
#                     val = [str(x) for x in val]
#                     print val
#                     val = val[2:8]
#                     print val
#                     val.insert(0, tableName)
#                     print tuple(val)
#                     query = "INSERT INTO %s VALUES ('%s')" % tuple(val)
#                     try:
#                         cur.execute(query)
#                     except psycopg2.Error as e:
#                         print e.pgerror
#                         pass
#     else:
#         print "Sorry Buddy, No database connection"

if __name__ == '__main__':
    # try:
    #     conn=psycopg2.connect("dbname='shalini' user='root' password='shalini'")
    # except:
    #     conn = None
    from django.conf import settings
    try:
        conn=psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (settings.US_CENSUS_DB['NAME'], 
        settings.US_CENSUS_DB['USER'], settings.US_CENSUS_DB['PASSWORD'], settings.US_CENSUS_DB['HOST'],
        settings.US_CENSUS_DB['PORT']))
    except psycopg2.Error as e:
        conn = None
    GeoCode(conn)
    Topic(conn)
    Characteristics(conn)

