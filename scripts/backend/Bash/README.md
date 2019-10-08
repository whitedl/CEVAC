# Bash scripts
Below is a brief synopsis of each bash script.

* `append_tables.sh`
  * Executes [`CEVAC_CACHE_APPEND`](https://github.com/whitedl/CEVAC/wiki/Data-Flow#cevac_cache_init-and-cevac_cache_append) for all HIST_VIEW tables in [CEVAC_TABLES](https://github.com/whitedl/CEVAC/wiki/Data-Flow#cevac_tables)
* `bootstrap.sh`
  * Used to add a new [BuildingSName]_[Metric] pipeline to the ecosystem.
  * Deletes all caches of a table and removes from [CEVAC_TABLES](https://github.com/whitedl/CEVAC/wiki/Data-Flow#cevac_tables) (see `delete.sh`)
  * Creates the various Ages of a pipeline (see [`CEVAC_VIEW`](https://github.com/whitedl/CEVAC/wiki/Data-Flow#cevac_view))
  * Creates a HIST_CACHE table (see [`CEVAC_CACHE_INIT`](https://github.com/whitedl/CEVAC/wiki/Data-Flow#cevac_cache_init-and-cevac_cache_append))
  * Creates a CSV and uploads it into LASR (see `lasr_append.sh` and `table_to_csv_append.sh`.
  * There is an entire wiki page dedicated to [bootstrapping](https://github.com/whitedl/CEVAC/wiki/Bootstrapping-the-CEVAC-Tables-Ecosystem).
* `CREATE_ALL_VIEWS.sh`
  * Executes `CREATE_VIEW.sh` for all Ages (e.g. PXREF, HIST, LATEST, etc)
  * See [CEVAC_VIEW](https://github.com/whitedl/CEVAC/wiki/Data-Flow#cevac_view) for more information.
* `CREATE_CUSTOM.sh`
  * Used to gather table structure metadata and add a new Custom pipeline into CEVAC_TABLES
  * Executes `CEVAC_CUSTOM_HIST`
* `create_standard_all.sh`
  * Driver script to recreate all standard [BuildingSName]_[Metric] views.
  * Not meant for everyday use (useful for debugging)
  * Calls `CREATE_ALL_VIEWS.sh` for all existing standard (not custom) tables
* `CREATE_VIEW.sh`
  * Executes [`CEVAC_VIEW`](https://github.com/whitedl/CEVAC/wiki/Data-Flow#cevac_view) for a given BuildingSName, Metric, and Age (e.g. WATT TEMP HIST)
  * Not usually used directly by a person (i.e. mostly called by driver scripts like `bootstrap.sh`)
* `custom_bootstrap_driver.sh`
  * Driver for debugging.
  * Calls `bootstrap.sh` for all standard tables.
  * Not meant for normal use
* `delete.sh`
  * Deletes all caches of [BuildingSName]_[Metric] tables
  * Deletes local CSV stored in /srv/csv/
* `exec_sql_script.sh`
  * Executes any given SQL script
  * Useful for long SQL queries
* `exec_sql.sh`
  * Executes any given SQL query (via command line)
  * Useful for simple queries
* `lasr_append.sh`
  * Driver script which updates a CSV and uploads the newest data to LASR
