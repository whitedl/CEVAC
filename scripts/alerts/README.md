# Alerts
The alerts csv should follow the following format:
```
alert_name, type, message, database, column, time, day, month, condition, value, operation,
```
For instance:
```
alert_name, type,  message,            database,                column, num_entries, hour,      day, month, condition, value, operation,
watt steam, steam, The steam usage..., CEVAC_WATT_STEAM_LATEST, 5,                   20-24&0-6, 6-7, *,     >,         1400,  warning,
watt steam, steam, The steam usage..., CEVAC_WATT_STEAM_LATEST, 5,                   20-24&0-6, 6-7, *,     >,         1500,  alert,
```

## Types 
