## Classification of Alerts for CEVAC

- Grouping / Prioritization of Alerts
  - Be able to tell if an alert is **<u>Low</u>**, **<u>Medium</u>**, or **<u>High</u>** Priority
  - Need to:
    - **Specifically define all metrics to gather regarding Alerts**
    - [x] Assign priority
    - [x] Group Similar Alerts
    - [x] Order alerts appropriately by `Total Calculated Importance`

#### Types of Errors:
  - Air handler sensor
  - CO2
  - Power Alerts
  - Temperature alerts
---   
#### Workflow:
  1. Alert system generates Alert
     - Time alerts: the sensor hasn't reported in a certain amount of time
     - Temperature Alerts: the temperature is reporting too high
     - Absolute Value: the sensor is outside of a range
  2. Document the alert
  3. Aggregate all active Alerts
     - 'Groups' of alerts are placed together and then shown in order of rank
     - ranking by importance
       - initial importance of the alert
       - time the alert has been active
