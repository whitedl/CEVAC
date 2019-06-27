
# Alerts
The alerts csv should follow the following format:
`alert_name, type, alias, units, alert_message, bldg_std, bldg_disp, database, column, sort_column, num_entries, time_dependent, occupancy_status, condition, value, alert_type, comments`
## Info
`alert_parameters.csv` is interpreted by `alert_system.py` which populates the table
`CEVAC_ALL_ALERTS_HIST`. Current, non-acknowledged alerts are displayed on the
controlboard to be acknowledged. 
## Example
A full example is located in `alert_parameters.csv`
```
alert_name, type, alias, units, alert_message, bldg_std, bldg_disp, database, column, sort_column, num_entries, time_dependent, occupancy_status, condition, value, alert_type, comments
Watt_CO2_warning, CO2, *, ppm, <alias> exceeds 1000 ppm., WATT, Watt, CEVAC_WATT_IAQ_LATEST, ActualValue, UTCDateTime, 1, 1, 1, >, 1000, warning,
Watt_CO2_alert, CO2, *, ppm, <alias> exceeds 2000 ppm., WATT, Watt, CEVAC_WATT_IAQ_LATEST, ActualValue, UTCDateTime, 1, 0, *, >, 2000, alert
```

---

The following is deprecated.
# Alerts
The alerts csv should follow the following format:
```
alert_name, type, alias, unit, message, building, database, column, sort_column, num_entries, hour, day, month, condition, value, operation,
```
For instance:
```
alert_name, type,  unit, message,            building, database,                column,      sort_column, num_entries, hour,      day, month, condition, value, operation,
watt steam, steam, kbtu, The steam usage..., WFIC,     CEVAC_WATT_STEAM_LATEST, ActualValue, UTCDateTime, 3,                  0-6&20-23, 6-7, *,     >,         1400,  warning,
```

## Types
* `alert_name` is a string describing the name of the alert
* `type` is a string describing the type of the alert
* `unit` is a string describing the units of the value
* `message` is a string describing the alert message
* `building` is a string describing the building for the alert
* `database` is a string describing database to check
* `column` is a string describing the column of the value
* `sort_column` is a string describing the column for the data to be sorted by
* `num_entries` is a string describing the number of entries to check
* `hour` is a string describing the hour(s) to check
* `day` is a string describing the day(s) to check
* `month` is a string describing the month(s) to check
* `condition` is a string describing the conditional
* `value` is a string describing the value for the conditional
* `operation` is a string describing the operation for the alert to accomplish
* `alias` is TODO

## Setting up the Cron Job
* `CEVAC_ALL_ALERTS_HIST`
  * This cron job should run every 10 minutes, `0/10 * * * * python3 alert_system.py`
	* Requirements
		* Python 3
		* Modules `pypyodbc`, `pytz`, `json`, `csv`
	* Setup
		* A logging directory must be made and replaces the `LOGGING_PATH` variable
		in `alert_system.py`
		* The `Alert Parameters (Working).csv` conditions csv path should replace
		the `CONDITIONS_FPATH` variable in `alert_system.py`
		  * The conditions csv can also be renamed if reflected in the correct
			`fname` variable
