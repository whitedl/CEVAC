# Alerts
The alerts csv should follow the following format:
```
Alert, Measure, Database, Time, Day, Month, Condition, Operation, Note
```
where `Alert` is the count of alerts, `measure` is the value type for warning,
`Time` is a time range for the alert, `Day` is a day of the week range for the
alert, `Month` is a month of the year range for the alert, `Condition` is an
actual condition for the alert, `Operation` is the warning type for the alert,
and `Note` is for noting (unused by scripting).

For instance:
```
Alert, Measure, Database,          Time,        Day, Month,   Condition, Operation, Note
1,     Water,   X_WATT_WATER_HIST, 00:00-06:00, any, any,     >10,       Warning,   .
2,     Steam    X_WATT_STEAM_HIST, any,         any, apr-nov, >200,000,  Alert,     .
```
