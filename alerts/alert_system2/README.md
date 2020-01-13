# Alerts
This is the second generation of the alert system. This program 
handles locating and documenting anomalies, emailing issues, 
and the machine-learning system for the alert system. 
All processes can be run from `main.py` with varying flags. 

## Executing
### Options and Flags
* Flags are enumerated via `python3 main.py -h`
```
usage: main.py [-h] [--log LOG] [--alerts] [--times TIMES] [--send] [--email]
               [--web] [--emailtime EMAILTIME] [--cache] [--machinelearning]
               [--queue] [--verbose]

Alert System v2. This alert system is heavily modular, allowing options to be
passed via the command line, as opposed to being burried in scripts.

optional arguments:
  -h, --help            show this help message and exit
  --log LOG, -L LOG, -l LOG
                        set log to True or False
  --alerts, -a, -A      check alerts currently
  --times TIMES, -t TIMES, -T TIMES
                        if set, checks alerts for different time periods where
                        possible
  --send, -s, -S        send anomalies to our database
  --email, -e, -E       send email of anomalies
  --web, -w, -W         update email as web page (wfic-
                        cevac1/cevac_alerts/alerts.html)
  --emailtime EMAILTIME, -et EMAILTIME, -ET EMAILTIME
                        set hours of anomalies to send via email[Default=24]
  --cache, -c, -C       update the cache before checking alerts
  --machinelearning, -ml, -ML
                        run machine learning algorithm after checking alerts
  --queue, -q, -Q       read queue for alerts instead of all alerts
  --verbose, -v, -V     printing
```

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

