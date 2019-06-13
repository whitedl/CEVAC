# ben_sql_api.py
## Used to verify data in our sql database and bring it in as python
## with little hassle
import urllib.request
import urllib.parse
import json

class Query:
    def __init__(self, sql_command):
        """
        Turn a SELECT sql command into data
        """
        if "SELECT" in sql_command.upper():
            self._command = sql_command
            self.query = self.command_to_query(self._command)
            self.json_list = self.request_data(self.query)
        else:
            self._command = None
            self.query = None
            self.json_list = []

    def command_to_query(self, sql_command):
        """
        Returns a query-able string from a sql command
        """
        req = "http://wfic-cevac1/requests/query.php?q="
        return req + urllib.parse.quote_plus(sql_command)

    def request_data(self, query):
        """
        Requests data
        """
        data = urllib.request.urlopen(query)
        data_readable = data.read().decode('utf-8').replace("}{","} {")
        data_list = data_readable.split("} {")
        json_list = []
        for i,d in enumerate(data_list):
            d = d if d[0] == "{" else "{" + d
            d = d if d[-1] == "}" else d + "}"
            json_list.append(json.loads(d))
        return json_list

    def as_dict(self,key=None):
        """
        Returns dictionary of data, keyed in as id or key
        """
        d = {}
        # Validate key in every dict
        if key != None:
            for data in self.json_list:
                if key not in data.keys():
                    key = None

        # Make into dict
        if key == None:
            for i,data in enumerate(self.json_list):
                d[i] = data
        else:
            for data in self.json_list:
                d[data[key]] = data

        return d
