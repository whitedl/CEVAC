# Alerts
The alerts csv should follow the following format:
```
alert_name, type, unit, message, building, database, column, sort_column, num_entries, hour, day, month, condition, value, operation,
```
For instance:
```
alert_name, type,  unit, message,            building, database,                column,      sort_column, num_entries, hour,      day, month, condition, value, operation,
watt steam, steam, kbtu, The steam usage..., WFIC,     CEVAC_WATT_STEAM_LATEST, ActualValue, UTCDateTime, 3,                  0-6&20-23, 6-7, *,     >,         1400,  warning,
```

## Types
* `alert_name` is a string describing the name of the alert
* `type` is a string describing the name of the alert
* `unit` is a string describing the name of the alert
* `message` is a string describing the name of the alert
* `building` is a string describing the name of the alert
* `database` is a string describing the name of the alert
* `column` is a string describing the name of the alert
* `sort_column` is a string describing the name of the alert
* `num_entries` is a string describing the name of the alert
* `hour` is a string describing the name of the alert
* `day` is a string describing the name of the alert
* `month` is a string describing the name of the alert
* `condition` is a string describing the name of the alert
* `value` is a string describing the name of the alert
* `operation` is a string describing the name of the alert
