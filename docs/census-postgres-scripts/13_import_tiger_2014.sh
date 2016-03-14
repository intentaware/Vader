#!/bin/bash
SQLHOME=/home/ubuntu/sql
cd /mnt/tmp/tiger2014

if [ -z $PGHOST ]; then
    echo "You must set PGHOST environment variable to the hostname of the PostgreSQL server to operate on."
    exit 1
fi

for i in **/*.zip
do
    unzip -q -n $i -d `dirname $i`
done

psql -h $PGHOST -d us_census -U census -c "DROP SCHEMA IF EXISTS tiger2014; CREATE SCHEMA tiger2014;"
psql -h $PGHOST -d us_census -U census -c "ALTER SCHEMA tiger2014 OWNER TO census;"

for i in CBSA CD COUNTY CSA PLACE STATE ELSD SCSD ZCTA5 COUSUB PUMA SLDL SLDU AIANNH AITS ANRC BG CNECTA CONCITY METDIV NECTA NECTADIV SUBMCD TBG TTRACT TABBLOCK TRACT UAC UNSD
do
    echo "convert shp file to postgis schema"
    one_shapefile=`ls -a $i/*.shp | head -n 1`

    echo "Start by preparing the table"
    shp2pgsql -W "latin1" -s 4326 -p -I $one_shapefile tiger2014.$i > $SQLHOME/$i.sql

    echo "appending all the geometries"
    for j in $i/*.shp
    do
        shp2pgsql -W "latin1" -s 4326 -a $j tiger2014.$i >> $SQLHOME/$i.sql
    done

    echo "load into PostgreSQL"
    psql -d us_census -h $PGHOST -U census -q -f $SQLHOME/$i.sql

    echo "removing temporary sql file $i.sql"
    rm -rf $SQLHOME/$i.sql

    if [ $? -ne 0 ]
    then
        echo "Couldn't import $i.sql."
        exit 1
    fi
done
