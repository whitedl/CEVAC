# Alerts
## About
The alert system is designed to be abstract and modular as to fit as many
use-cases as possible. Due to this, it has high complexity. Alerts search for
3 things as of now:
1. Specific values
2. Relative temperature setpoints
3. Report times

## `alert_system.py`
* Populates the `CEVAC_ALL_ALERTS_HIST_RAW` table with events read from
`alert_parameters.csv` located in `CEVAC/alerts`
* Run `python3 alert_system.py`
## `alert_mail.py`
* Run `python3 run.py alertmail` or `python3 run_script.py alert_mail.py`
* Mails top 100 alerts from the past day

## Setting up the Cron Job
* `CEVAC_ALL_ALERTS_HIST`
  * This cron job should run every 15 minutes, `*/15 * * * * python3 alert_system.py`
	* Requirements
		* Python 3
		* Modules `pytz`, `json`, `csv`, `croniter`, `urllib`
	* Setup
		* A logging directory must be made and replaces the `LOGGING_PATH` variable
		in `alert_system.py`
		* The `alert_parameters.csv` conditions csv path should replace
		the `CONDITIONS_FPATH` variable in `alert_system.py`
		  * The conditions csv can also be renamed if reflected in the correct
			`fname` variable
    * Make sure the "static" variables at the beginning of the script fit the
    use case (e.g. `SEND = True` if you want the alerts to be sent to the
    database)
