# WAP
`importer.py` uses `safe_move.py` to populate tables `CEVAC_WATT_WAP_HIST` and
`CEVAC_WATT_WAP_FLOOR_HIST`.  `daily_count.py` populates table
`CEVAC_WATT_WAP_DAILY`.

For the thought process Harrison and Drew had, consult
[our experiments](Experimentation.md).

## Tables
### `CEVAC_WATT_WAP_HIST`
Has columns `time` (UTC), `name`, `ssid`, `total_duration`,
`predicted_occupancy`, and `unique_users`. `name` is an id for the wireless
access point. `ssid` is the name of the network. `total_duration` is the number
of minutes individuals were on a wap during a 30 minute period.
`predicted_occupancy` is the float of people-hours (`total_duration`/60).
`unique_users` is the count of unique individuals on a wap during a 30 minute
period. Before 06/25/19, the period was an hour. This does not hold data before
May 2019.
### `CEVAC_WATT_WAP_FLOOR_HIST`
Has columns `UTCDateTime`, `floor`, `clemson_count`, and `guest_count`. The
`clemson` and `guest` columns are integer counts for the number of unique
individuals on a floor during a 30 minute period. Before 06/25/19, the period
was an hour. This does not hold data before May 2019.
### `CEVAC_WATT_WAP_DAILY`
Has columns `date`, `clemson`, and `guest`. The `clemson` and `guest` columns
are integer counts for the number of unique individuals inside the WFIC during
the day. This does not hold data before May 2019.

## Setting up the Cron Jobs
* `CEVAC_WATT_WAP_DAILY`
  * This cron job should run daily at 2 AM, `0 2 * * * python3 daily_count.py`
	* Requirements
		* Python 3
		* Modules `pypyodbc`, `pytz`, `json`, `csv`
	* Setup
		* *N/A*
