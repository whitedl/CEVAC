"""Pull data for ml use."""
import os

fname = "sample1.csv"
command = "SELECT TOP 100 * FROM CEVAC_ALL_ALERTS_HIST_RAW"
os.system(f"/cevac/scripts/exec_sql.sh \"{command}\" "
          f"{fname}")
