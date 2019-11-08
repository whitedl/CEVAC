"""Machine learning algorithm."""
import pyodbc
from pandas import DataFrame


class ML:
    """ML suite for connected issues and finding root causes."""

    def __init__(self):
        """Initialize data and connections."""
        self.start_weight = 0.5
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=130.127.218.11;DATABASE=WFIC-CEVAC;UID=wficcm;PWD=5wattcevacmaint$')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM test")
        data = cursor.fetchall() # List of tuples
        readable_data = DataFrame(data)

        self.nodes = [l.psid for l in []]  # TODO
        self.edges = {}  # Map from psid1 to Map of psid2 to edge value

    def add_nodes(self, alerts):
        """Manage new nodes from alerts.

        Add new nodes if alert is not a node.
        Manage edge weights for current alerts.
        """
        new_nodes = [Node(alert) for alert in alerts]

        # Connect new nodes
        for i, node1 in enumerate(new_nodes):
            for j, node2 in enumerate(new_nodes):

                # Ensures you only connect to that which you haven't
                met_me = False
                if (node1.psid == node2.psid):
                    met_me = True
                elif not met_me:
                    continue

                if node1 in self.edges:
                    if node2 in self.edges[node1]:
                        continue
                    else:
                        self.edges[node1][node2] = self.start_weight
                        if node2 in self.edges:
                            self.edges[node2][node1] = self.start_weight
                        else:
                            self.edges[node2] = {node1: self.start_weight}
                else:
                    self.edges[node1] = {node2: self.start_weight}
                    if node2 in self.edges:
                        self.edges[node2][node1] = self.start_weight
                    else:
                        self.edges[node2] = {node1: self.start_weight}


        for i, node in enumerate(new_nodes):
            if node.psid in nodes:
                for edge in edges:
                    pass
            else:
                pass
        return None

    def send(self):
        """Send nodes and edges back to database."""
        pass

    def queries(self):
        """Execute necessary queries."""
        pass

    def decrease_weight(self, edge, node1, node2):
        """Decrease edge weight."""
        edge -= 0
        return edge

    def increase_weight(self, edge, node1, node2):
        """Increase edge weight."""
        edge += 0
        return edge

    def __del__(self):
        """Deconstruct ML."""
        self.conn.close()


class Node:
    """Node for ML."""

    def __init__(self, node_row):
        """Init node."""
        pass


class Edge:
    """Edge for ML."""

    def __init__(self, edge_row):
        """Init edge."""
        pass
