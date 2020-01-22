"""
Handle which issues to ignore. 

Ignored sensors are sensors that have 
been flagged with `decomissioned` in 
the table `CEVAC_KNOWN_ISSUES`. 
"""

import pyodbc
import pandas as pd
from tools import verbose_print


class KnownIssues:
    """Represents known issues to ignore."""
    
    def __init__(self, conn : pyodbc.Connection):
        """Initialize known issues."""
        data = pd.read_sql_query(
            "SELECT * FROM CEVAC_KNOWN_ISSUES",
            conn
        )
        self.alias_psid = {}
        for i in range(len(data)):
            if 'decomissioned' in data['Code'][i].lower():
                self.alias_psid[data['PSID_Alias'][i]] = None

    def check_aliaspsid(self, aliaspsid : str) -> bool:
        """True if aliaspsid should be ignored."""
        return (aliaspsid in self.alias_psid)

    def __str__(self) -> str:
        return (
            f"KNOWNISSUES {self.alias_psid}"
        )

    def __repr__(self) -> str:
        return (
            f"KNOWNISSUES #({len(self)})"
        )

    def __len__(self) -> int:
        return len(self.alias_psid)

    def __getitem__(self, position : int) -> str:
        return list(self.alias_psid.keys())[position]

    def __contains__(self, item : str) -> bool:
        return (item in self.alias_psid)

    def __nonzero__(self) -> bool:
        if len(self) > 0:
            return True
        return False

    def __bool__(self) -> bool:
        return self.__nonzero__()


"""
      /##.*/
     /#%&&%#/
    ./%%%&%%#
    %%%%&%&%%#
   %&&  %%%&%%.
   %&%  &%%&%%*
   *%&@&@%&%%(
     %%%%%%%%
"""
