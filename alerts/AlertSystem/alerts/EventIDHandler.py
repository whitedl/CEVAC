"""
EventIDHandler handles reading and 
assigning EventIDs to new anomalies.

By calling the class, one can commit
the additions and removals of EventIDs
from the table `CEVAC_ALERTS_EVENTS_IDS`. 
"""

import pyodbc
import pandas as pd
from tools import verbose_print


class EventIDHandler:
    """Ease use of event IDs."""
    
    def __init__(
            self,
            conn : pyodbc.Connection,
            debug=False,
            verbose=False
    ):
        self.debug = debug
        self.verbose = verbose
        
        self.new_events = {}
        self.conn = conn
        self.data = pd.read_sql_query(
            f"SELECT * FROM CEVAC_ALERTS_EVENTS_IDS",
            self.conn
        )
        self.max_id = self.get_max_id()
        self.event_to_id = self.get_event_to_id(self.data)
        self.remove_ids = []

    def remove_event_id(
            self,
            alias : str,
            psid : int,
            alert : dict
    ) -> None:
        name = f"{alias} {psid} {alert['type']}"
        if name in self.event_to_id:
            self.remove_ids.append(self.event_to_id[name])
        return None

    def commit_removes(self) -> None:
        cursor = self.conn.cursor()
        for eid in self.remove_ids:
            if not self.debug:
                cursor.execute(
                    f"DELETE FROM CEVAC_ALERTS_EVENTS_IDS "
                    f"WHERE EventID = {eid}"
                )
                cursor.commit()
            else:
                verbose_print(
                    self.verbose,
                    f"DELETE FROM CEVAC_ALERTS_EVENTS_IDS "
                    f"WHERE EventID = {eid}"
                )
        
        cursor.close()
        return None

    def add_event_id(self, name : str, eid : int) -> None:
        self.new_events[name] = eid
        return None

    def commit_adds(self) -> None:
        cursor = self.conn.cursor()
        for name in self.new_events:
            eid = self.new_events[name]
            if not self.debug:
                cursor.execute(
                    f"INSERT INTO CEVAC_ALERTS_EVENTS_IDS "
                    f"(EventName, EventID) "
                    f"VALUES ('{str(name)}', {int(eid)})"
                )
                cursor.commit()
            else:
                verbose_print(
                    self.verbose,
                    f"INSERT INTO CEVAC_ALERTS_EVENTS_IDS "
                    f"(EventName, EventID) "
                    f"VALUES ('{str(name)}', {int(eid)})"
                )
        cursor.close()
        return None

    def get_event_to_id(self, data : pd.DataFrame) -> dict:
        """Return map of event to id"""
        d = {}
        for i in range(len(data)):
            d[data["EventName"][i]] = data["EventID"][i]
        return d

    def get_max_id(self) -> int:
        """
        Returns the maximum EventID so far.
        """
        so_far = 1
        for eid in self.data["EventID"]:
            so_far = max(so_far, eid)
        return so_far + 1

    def assign_event_id(
            self,
            alert : dict,
            alias : str,
            psid : int
    ) -> int:
        """Assign event id."""
        if str(alert) == "All Clear":
            key = f"{alias} All Clear"
        else:
            key = f"{alias} {psid} {alert['type']}"
        if key in self.event_to_id:
            return self.event_to_id[key]
        else:
            this_id = self.max_id
            self.max_id += 1
            self.add_event_id(key, this_id)
            return this_id

    def __str__(self) -> str:
        return (
            f"EVENTIDS CHANGES: \n"
            f"Adding {self.new_events}\n"
            f"Removing {self.remove_ids}"
        )

    def __repr__(self) -> str:
        return (
            f"EVENTID HANDLER: "
            f"ADD#({len(self.new_events)}) "
            f"REM#({len(self.remove_ids)}) "
            f"MAXID#({self.max_id})"
        )

    def __add__(self, other : "EventIDHandler") -> "EventIDHandler":
        """
        Add two EventIDHandler's together to combine 
        events to add and remove.
        """
        new_eidhandler = EventIDHandler(
            self.conn, debug=self.debug, verbose=self.verbose
        )
        new_eidhandler.remove_ids = (
            self.remove_ids + other.remove_ids
        )
        new_eidhandler.new_events.update(self.new_events)
        new_eidhandler.new_events.update(other.new_events)
        return new_eidhandler

    def __len__(self) -> int:
        return len(self.new_events)

    @property
    def next_id(self) -> int:
        return self.max_id

    @property
    def new_ids(self) -> int:
        return len(self.new_events)

    @property
    def old_ids(self) -> int:
        return len(self.remove_ids)

    def __getitem__(self, position : int) -> str:
        return list(self.new_events.keys())[position]

    def __eq__(self, other : "EventIDHandler") -> bool:
        return False

    def __call__(self) -> None:
        self.commit_remove()
        self.commit_adds()
        return None

    def __contains__(self, eid : int) -> bool:
        """True if eid in new_events"""
        return (eid in self.new_events)

    def __reversed__(self) -> "EventIDHandler":
        return self

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
