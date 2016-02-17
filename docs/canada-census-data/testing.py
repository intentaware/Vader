from django.conf import settings
import psycopg2
import csv

try:
    conn=psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (settings.US_CENSUS_DB['NAME'], 
	settings.US_CENSUS_DB['USER'], settings.US_CENSUS_DB['PASSWORD'], settings.US_CENSUS_DB['HOST'],
    settings.US_CENSUS_DB['PORT']))
except:
	conn = None


# try:
#     conn=psycopg2.connect("dbname='shalini' user='root' password='shalini'")
# except:
#     conn = None

if conn:
    conn.set_isolation_level(0)
    cur = conn.cursor()
    with open('/home/shalini/csv/shalini.CSV') as f:
        reader = csv.reader(f)
        tableName = 'GeoId'
        cur.execute("CREATE TABLE IF NOT EXISTS %s();"  % (tableName))
        for idx, val in enumerate(reader):
            if idx == 0:
                # for column in val:
                #     pass
                query = "ALTER TABLE %s ADD %s text UNIQUE, ADD %s text UNIQUE;" % (tableName, val[0], val[1])
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