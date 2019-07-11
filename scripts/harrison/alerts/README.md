# Alerts
## `alert_system.py`
* Populates the `CEVAC_ALL_ALERTS_HIST_RAW` table with events read from
alert_parameters.csv
* Run `python3 alert_system.py`
## `alert_mail.py`
* Run `python3 run.py alertmail` or `python3 run_script.py alert_mail.py`

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
