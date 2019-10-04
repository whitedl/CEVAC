## Classification of Alerts for CEVAC

- Grouping / Prioritization of Alerts
  - Be able to tell if an alert is **<u>Low</u>**, **<u>Medium</u>**, or **<u>High</u>** Priority
  - Need to:
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
---
#### Alert Classification
A basic alert classification procedure:
1. Manually build table mapping a unique alert type to another (or message),
with weight(s)
2. Build graph of unique alert types (nodes) connected via the weights (edges)
3. Trace through the graph if edges exceed a value, and sort the end results
by some weight
4. Insert the sorted results into a database
---
#### Breakdown
1. Decide outputs and inputs
   * Outputs: unique alerts -> unique alerts, unique alerts -> message,
   * Inputs: 
2. Determine best approach
3. Profit
