import uuid
import time


class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.routing_table = {}
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def send_rreq(self, destination_id):
        rreq_id = uuid.uuid4()
        rreq_message = {
            'type': 'RREQ',
            'rreq_id': rreq_id,
            'source_id': self.node_id,
            'destination_id': destination_id,
            'hop_count': 0
        }
        self.broadcast_message(rreq_message)

    def send_rrep(self, rreq_message, next_hop):
        rrep_message = {
            'type': 'RREP',
            'rreq_id': rreq_message['rreq_id'],
            'source_id': rreq_message['source_id'],
            'destination_id': self.node_id,
            'next_hop': next_hop,
            'hop_count': rreq_message['hop_count'] + 1
        }
        self.send_message(next_hop, rrep_message)

    def handle_rreq(self, rreq_message):
        if rreq_message['destination_id'] == self.node_id:
            self.send_rrep(rreq_message, rreq_message['source_id'])
        else:
            rreq_message['hop_count'] += 1
            self.broadcast_message(rreq_message)

    def handle_rrep(self, rrep_message):
        if rrep_message['source_id'] == self.node_id:
            self.routing_table[rrep_message['destination_id']] = rrep_message['next_hop']
        else:
            self.send_message(rrep_message['next_hop'], rrep_message)

    def broadcast_message(self, message):
        for neighbor in self.neighbors:
            self.send_message(neighbor, message)

    def send_message(self, neighbor, message):
        # Simulate message sending
        print(f"Node {self.node_id} sends {message['type']} to Node {neighbor}")
        # Simulate message handling by neighbor
        neighbor.handle_message(message)

    def handle_message(self, message):
        if message['type'] == 'RREQ':
            self.handle_rreq(message)
        elif message['type'] == 'RREP':
            self.handle_rrep(message)


# Example usage
node1 = Node(1)
node2 = Node(2)
node3 = Node(3)

node1.add_neighbor(node2)
node2.add_neighbor(node1)
node2.add_neighbor(node3)
node3.add_neighbor(node2)

node1.send_rreq(3)

time.sleep(1)  # Simulate network delay