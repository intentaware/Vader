echo "Importing Unified meta data"
cat /home/ubuntu/census-table-metadata/precomputed/unified_metadata.csv | psql -d us_census -h $PGHOST -U census -v ON_ERROR_STOP=1 -q -c "COPY public.census_tabulation_metadata FROM STDIN WITH csv ENCODING 'utf8';"

if [[ $? != 0 ]]; then
    echo "Failed importing unified metadata."
    exit 1
fi
