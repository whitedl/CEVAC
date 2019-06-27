# WAP Cron Job
`importer.py` uses `safe_move.py` to populate tables `CEVAC_WATT_WAP_HIST` and
`???`.  
`daily_count.py` populates table `CEVAC_WATT_WAP_DAILY` for the columns `date`,
`clemson`, and `guest`. The `clemson` and `guest` columns are integer counts for
the number of unique individuals inside the WFIC during the day.

## CEVAC_WATT_WAP_HIST
This database contains time, name, SSID, wap-hours, predicted occupancy, and
a count of unique user IDs. A non-current version is stored on lasr.

## Setting up the Cron Jobs
* `CEVAC_WATT_WAP_DAILY`
  * This cron job should run daily at 2 AM, `0 2 * * * python3 daily_count.py`
	* Requirements
		* Python 3
		* Modules `pypyodbc`, `pytz`, `json`, `csv`
	* Setup
		* *N/A*
