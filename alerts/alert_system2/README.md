# Alerts
This is the second generation of the alert system. This program 
handles locating and documenting anomalies, emailing issues, 
and the machine-learning system for the alert system. 
All processes can be run from `main.py` with varying flags. 

## Executing
### Options and Flags
* Flags are enumerated via `python3 main.py -h`

## About
### Checking Anomalies
The alert system is designed to be abstract and modular as to 
fit as many use-cases as possible. Due to this, it has high 
complexity. Alerts search for 3 different issues:
1. Variance from specific values
2. Relative temperature setpoints disagreements
3. Report times over a time delta

These anomalies can be found via the `-a` flag. In order to write the 
anomalies to the CEVAC SQL database, use the `-s` flag. 

### Sending Emails
Emails can be sent via the `-e` flag. 

### Debugging
To make the alert system more transparent, use the `-v` flag for 
verbosity. 

### ML
#### Iteration 1
#### Iteration ...

