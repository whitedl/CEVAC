# Scripts
These scripts were written by Harrison Hall for various data accumulation and
manipulation. `tiling` handles windows window tiling, as used on the emergency
response screen. `wap` handles data aggregation from the WATT building server.
`alerts` handles the automated alert system.


## `bsql.py`
* `bsql` is a module used for querying the cevac server for data
* `help(bsql)` will show the docstrings for the `Query` class
* `Query("Select * FROM CEVAC_WATT_WAP_DAILY_HIST").to_json()` will return a
dictionary of data made from the query
