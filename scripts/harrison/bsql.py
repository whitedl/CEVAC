"""Modify sql data on linux."""

import os
import csv
import json


class Query:
    """Turn a SELECT query into data."""

    def __init__(self, sql_command):
        """Turn a SELECT sql command into data."""
        if "SELECT" in sql_command.upper():
            self.command = sql_command
            self.json_list = self.request_data(self.command)
        else:
            self.command = None
            self.query = None
            self.json_list = []

    def request_data(self, command):
        """Request data."""
        os.system(f"/home/bmeares/scripts/exec_sql.sh \"{command}\" "
                  "temp1_csv.csv")
        json_string = ""
        headers = {}
        with open("/cevac/cache/temp1_csv.csv", "r") as temp_csv:
            csvfile = csv.reader(temp_csv)
            for i, row in enumerate(csvfile):
                if i == 0:
                    for j, item in enumerate(row):
                        headers[j] = item
                else:
                    temp_dict = {}
                    try:
                        for j, item in enumerate(row):
                            temp_dict[headers[j]] = item
                        json_string += str(temp_dict)
                    except Exception:
                        continue
        data_readable = json_string.replace("\'", "\"")
        data_list = data_readable.split("}{")
        return self._data_list_to_dict_list(data_list)

    def _data_list_to_dict_list(self, data_list):
        dict_list = []
        for i, d in enumerate(data_list):
            d = d if d[0] == "{" else "{" + d
            d = d if d[-1] == "}" else d + "}"
            dict_list.append(json.loads(d))
        data_list = []
        for sd in dict_list:
            try:
                dl = []
                for k in sd:
                    dl.append(sd[k])
                data_list.append(dl)
            except Exception:
                pass
        return data_list

    def as_dict(self, key=None):
        """Return dictionary of data, keyed in as id or key."""
        d = {}
        # Validate key in every dict
        if key is not None:
            for data in self.json_list:
                if key not in data.keys():
                    key = None

        # Make into dict
        if key is None:
            for i, data in enumerate(self.json_list):
                d[i] = data
        else:
            for data in self.json_list:
                d[data[key]] = data

        return d

    def as_json_dict(self):
        """Return dictionary of data, with dicts instead of lists."""
        d = {}
        return d


class INSERT:
    """INSERT a string into a sql table."""

    def __init__(self, COMMAND, fname="insert_bsql.sql"):
        """Complete the insertion."""
        self.success = False
        if "INSERT" not in COMMAND:
            return self.success
        f = open(f"/home/bmeares/cache/{fname}", "w")
        f.write(COMMAND.replace(';', '\nGO\n'))
        f.close()
        os.system("/home/bmeares/scripts/exec_sql_script.sh "
                  f"/home/bmeares/cache/{fname}")
        os.remove(f"/home/bmeares/cache/{fname}")
        self.success = True
        return self.success


'''
        /##.*/
       /#%&&%#/
      ./%%%&%%#
      %%%%&%&%%#
     %&&  %%%&%%.
     %&%  &%%&%%*
     *%&@&@%&%%(
       %%%%%%%%
'''
