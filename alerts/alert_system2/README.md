# Alerts
This is the second generation of the alert system. This program handles locating and 
documenting anomalies, emailing issues, and the machine-learning system for the alert system. 
All processes can be run from `main.py` with varying flags. 
## Executing
### Flags
* `-l [true|false]` Sets log to true or false [default=True]
* `-a` Checks alerts currently
* `-t [NUMBER]` Runs the program for times in hour intervals for the past `[NUMBER]` of hours until 
present [default=0]
* `-s` Send anomalies to database
* `-e` Send email of anomalies
* `-et [NUMBER]` Emails current events from the past `[NUMBER]` of hours [default=24]
* `-c` Updates cache before checking emails
* `-ml` Runs the machine learning process

## About
### Tables
### Checking Anomalies
The alert system is designed to be abstract and modular as to fit as many
use-cases as possible. Due to this, it has high complexity. Alerts search for
3 different issues:
1. Variance from specific values
2. Relative temperature setpoints disagreements
3. Report times over a time delta
### Sending Emails
### ML

