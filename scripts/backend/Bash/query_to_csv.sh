#! /bin/bash
usage="Usage:
  -i input file location
  -o output location
  -q query
  -h help
"
while getopts i:q:o:h option; do
  case "${option}"
    in
    i) script_location=${OPTARG};;
    q) query=${OPTARG};;
    h) echo "$usage" && exit 1 ;;
    o) output_location=${OPTARG}
  esac
done
if [ -z "$script_location" ] && [ -z "$query" ]; then
  echo "$usage"
  exit 1
fi
if [ -z "$output_location" ] ; then
  output_location="/cevac/cache/sql_output.csv"
fi
if [ -z "$script_location" ] ; then
  script_location="/cevac/cache/csv_query_script.sql"
  echo "$query" > $script_location
fi

has_nocount=`cat "$script_location" | grep "SET NOCOUNT ON"`
if [ -z "$has_nocount" ] ; then
  sed -i '1s/^/SET NOCOUNT ON\n/' "$script_location"
fi

source /cevac/scripts/sql_env.sh
h="$SQL_HOST"
u="$SQL_USER"
db="$SQL_DB"
p="$SQL_PASS"

/opt/mssql-tools/bin/sqlcmd -S $h -U $u -d $db -P $p -i "$script_location" -W -o "$output_location" -s"," -w 700
sed 2d -i "$output_location"

echo "Results are stored in $output_location"

