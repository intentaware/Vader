import psycopg2
import csv

try:
    conn=psycopg2.connect("dbname='shalini12' user='root' password='shalini'")
except:
    conn = None

if conn:
    conn.set_isolation_level(0)
    cur = conn.cursor()
    with open('/path/to/csv/file') as f:
        reader = csv.reader(f)
        for idx, val in enumerate(reader):
            if idx == 0:
                tableName = ''.join(e for e in val[0] if e.isalnum())
                # tableName = ("").join(val[0].split(" "))
                query = "CREATE TABLE IF NOT EXISTS %s();"  % (tableName)
                try:
                    cur.execute(query)
                except psycopg2.Error as e:
                    print e.pgerror
                    pass
                print tableName
            elif idx == 1:
                for column in val:
                    pass
                    query = "ALTER TABLE %s ADD %s text;" % (tableName, column)
                    try:
                        cur.execute(query)
                    except psycopg2.Error as e:
                        print e.pgerror
                        pass
            else:
                val = [str(x) for x in val]
                val.insert(0, tableName)
                query = "INSERT INTO %s VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % tuple(val)
                try:
                    cur.execute(query)
                except psycopg2.Error as e:
                    print e.pgerror
                    pass
else:
    print "Sorry Buddy, No database connection"