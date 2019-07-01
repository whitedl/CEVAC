"""Script runner used for modular imports."""

from sys import argv

from alerts import alert_mail

script_table = {
    "alert_mail.py": alert_mail.main,
}

for arg in argv:
    if arg in script_table:
        script_table[arg]()
