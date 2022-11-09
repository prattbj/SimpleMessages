import pickle
"""
TCPPacket contains different types of packets that could be sent 
and received between the client and the server.
"""


class Packet:
    """
    Parent class. A packet of data.
    """
    def encode_packet(self):
        """
        Turns the packet into bytes.
        """
        return pickle.dumps(self)


class RegisterPacket(Packet):
    """
    Registers the user with the server.
    """
    def __init__(self, username: str, public_key: bytes):
        self.username = username
        self.public_key = public_key


class TextPacket(Packet):
    """
    Sends text to the server to be sent to a recipient.
    """
    def __init__(self, username: str, recipient: str, message_bytes: bytes):
        self.username = username
        self.recipient = recipient
        self.message_bytes = message_bytes


class ClientUpdatePacket(Packet):
    """
    Sends a dictionary of all users and their public keys as well
    as a dictionary of messages that are addressed to the
    client.
    """
    def __init__(self, users: dict, messages: dict):
        self.users = users
        self.messages = messages


class EmptyPacket(Packet):
    """
    A blank packet so that the server won't wait on information
    that isn't going to be sent.
    """
    def __init__(self):
        self.skip = True


def decode_packet(packet: bytes):
    """
    Takes in a packet that has been converted to a bytes object
    and returns a packet object.
    """
    return pickle.loads(packet)
