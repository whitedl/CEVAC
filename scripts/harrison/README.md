# Scripts
These scripts were written by Harrison Hall for various data accumulation and
manipulation. `tiling` handles windows window tiling, as used on the emergency
response screen. `wap` handles data aggregation from the WATT building server.
`alerts` handles the automated alert system. `chw` and `power` handle the
data aggregation from chilled water and power meters on the WATT building
server. `misc` holds arbitrary code that should be versioned "just in case."


## `generic_importer.py`
`generic_importer.py` is a csv importer script that is works on both linux
and windows. Simply change the modular variables at the beginning of the
program, modify the correct `ingest_file_<platform>` function and run the
program.


## `bsql.py`
* `bsql` is a module used for querying the cevac server for data
* `help(bsql)` will show the docstrings for the `Query` class
* `Query("Select * FROM CEVAC_WATT_WAP_DAILY_HIST").as_dict()` will return a
dictionary of data made from the query
  * Keys are integers 1-n
  * `.as_dict(key="UTCDateTime")` will make `UTCDateTime` the key in the
  dictionary


## `time_handler.py`
when inserting via `bsql`, a string is required. When querying via `bsql`,
strings are returned. UTC and EST conversion is another necessary conversion.
This can all be handled with `time_handler.py`.
