"""Machine learning algorithm."""


class ML:
    """ML suite for connected issues and finding root causes."""

    def __init__(self):
        """Initialize data and connections."""
        nodes = None  # TODO
	edges = None # TODO
	

    def add_nodes(self, alerts):
        """Manage new nodes from alerts.

        Add new nodes if alert is not a node.
        Manage edge weights for current alerts.
        """
        pass

    def send(self):
        """Send nodes and edges back to database."""
        pass

    def queries(self):
        """Execute necessary queries."""
        pass

    def decrease_weight(self, edge, node1, node2):
	edge -= 0
	return edge

    def increase_weight(self, edge, node1, node2):
	edge += 0
	return edge
