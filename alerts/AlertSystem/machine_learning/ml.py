"""Machine learning algorithm."""
import pyodbc
import pandas as pd


class ML:
    """ML suite for connected issues and finding root causes."""

    def __init__(self, anomalies, conn=None, verbose=False,
                 logging=None):
        """Initialize data and connections."""
        self.verbose = verbose
        self.conn = conn
        if conn is None:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=130.127.218.11;'
                'DATABASE=WFIC-CEVAC;'
                'UID=wficcm;'
                'PWD=5wattcevacmaint$'
            )

        self.logging = logging
        self.LOG = True
        if logging is None:
            self.LOG = False

        self.anomalies = {}
        for anomaly in anomalies:
            n = f"{anomaly.aliaspsid} {anomaly.alert_name}"
            self.anomalies[n] = anomaly

        if self.LOG:
            loggin.info("Starting ML Edges")
        data = pd.read_sql_query(
            "SELECT * FROM CEVAC_ALERTS_EDGES",
            self.conn
        )
        self.edges_to_update = {}
        for i in range(len(data)):
            if (data["Node1"][i] in self.anomalies or
                data["Node2"][i] in self.anomalies):

                combined_aliaspsid1 = (
                    data["Node1"][i] + data["Node2"][i]
                )
                combined_aliaspsid2 = (
                    data["Node2"][i] + data["Node1"][i]
                )
                e = Edge(i, data)
                self.edges_to_update[combined_aliaspsid1] = e
                self.edges_to_update[combined_aliaspsid2] = e


    def do_ml(self):
        """Run main ML process."""
        self.add_new_edges()
        self.adjust_weights()

    def add_new_edges(self):
        """Manage new nodes from alerts.

        Add new nodes if alert is not a node.
        Manage edge weights for current alerts.
        """
        # Connect new nodes
        for i, node1name in enumerate(self.anomalies):
            for j, node2name in enumerate(self.anomalies):
                if j <= i:
                    continue

                node1 = self.anomalies[node1name]
                node2 = self.anomalies[node2name]

                # Don't add edges if aliaspsid_alertnames are the same
                if node1 == node2:
                    continue

                # If edge exists, skip
                combined_name1 = (
                    self.get_node_name(node1) +
                    ' ' +
                    self.get_node_name(node2)
                )
                combined_name2 = (
                    self.get_node_name(node2) +
                    ' ' +
                    self.get_node_name(node1)
                )

                if combined_name1 in self.edges_to_update:
                    continue

                e = Edge(0, None, anomaly1=node1, anomaly2=node2)
                self.edges_to_update[combined_name1] = e
                self.edges_to_update[combined_name2] = e
        return None

    def adjust_weights(self):
        for edge_name in self.edges_to_update:
            edge = self.edges_to_update[edge_name]
            if (edge.node1 in self.anomalies and
                edge.node2 in self.anomalies):
                edge.times_together += 1
            else:
                edge.times_apart += 1

            alpha = edge.findAlpha()
            beta = 1 - alpha
            edge.weight = (
                alpha + beta*(
                        (edge.times_together - edge.times_apart) /
                        (edge.times_together + edge.times_apart)
                )
            )


        return None

    def send(self):
        """Send nodes and edges back to database."""
        for edge in self.edges_to_update:
            pass
        return None

    def queries(self):
        """Execute necessary queries."""
        return None

    def set_new_weights(self):
        for edge in self.edges:
            pass

    def decrease_weight(self, edge, node1, node2):
        """Decrease edge weight."""
        edge -= 0
        return edge

    def increase_weight(self, edge, node1, node2):
        """Increase edge weight."""
        edge += 0
        return edge

    def get_node_name(self, node):
        return node.aliaspsid + ' ' + node.alert_name



class Edge:
    """Edge for ML."""

    def __init__(self, i, data, anomaly1=None, anomaly2=None):
        """Init edge."""
        if anomaly1 is None and anomaly2 is None:
            self.node1 = data["Node1"][i]
            self.node2 = data["Node2"][i]
            self.weight = data["Weight"][i]

            self.times_together = data["Times_Together"][i]
            self.times_apart = data["Times_Apart"][i]
            self.anomaly1 = None
            self.anomaly2 = None
            self.BuildingSimilarity = data["BuildingSimilarity"][i]
            self.FloorSimilarity = data["FloorSimilarity"][i]
            self.MetricSimilarity = data["MetricSimilarity"][i]
        else:
            self.anomaly1 = anomaly1
            self.anomaly2 = anomaly2

            self.node1 = (
                anomaly1.aliaspsid + " " + anomaly1.alert_name
            )
            self.node2 = (
                anomaly2.aliaspsid + " " + anomaly2.alert_name
            )

            self.times_together = 1
            self.times_apart = 0

            #Building and Floor Comparison
            if (anomaly1.building == anomaly2.building):
                self.BuildingSimilarity = 1

                self.FloorSimilarity = (
                    1 -
                    abs(int(anomaly1.floor)-int(anomaly2.floor))*0.1
                    )
                        #Floor comparison in same building
                        #Arbitrary 0.1 to know how much we want to decrease
                        #with each floor of separation

            else:
                self.BuildingSimilarity = 0 #dif building value
                self.FloorSimilarity = 0 #dif building floor value

            #Metric Comparison
            if (anomaly1.alert["metric"] == anomaly2.alert["metric"]):
                self.MetricSimilarity = 1
            else:
                self.MetricSimilarity = 0

            self.weight = self.init_weight(anomaly1, anomaly2)

    def init_weight(self, anomaly1, anomaly2):
        """Initialize weight between nodes."""
        return self.findAlpha()

    def findAlpha(self):
        """Determine Alpha Value for Weight"""
        a = 0.5
        k = 0.1 #change constant
        a+= k*self.BuildingSimilarity
        a+= k*self.FloorSimilarity
        a+= k*self.MetricSimilarity
        return a
