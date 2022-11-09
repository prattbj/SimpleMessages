# Created by Benjamin Pratt on 11/8/2022
import socket
import TCPPacket


def main():
    """
    A server that sends and receives data.
    """
    # Port number
    port = 5000

    # Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('', port))

    # Stores user information and messages
    users = {}
    messages = {}
    while True:
        # Wait for a user to connect
        s.listen(1)
        # Get the connection and address of the user
        c, address = s.accept()
        # Get a packet containing a username and public key
        register = TCPPacket.decode_packet(c.recv(1024))
        # Initialize an update packet to be sent to the user
        update_packet = TCPPacket.ClientUpdatePacket({}, {})
        # Add the user to the dictionary of users
        users[register.username] = register.public_key
        # Add the user dictionary to the update packet
        update_packet.users = users
        # Try to get messages from the messages dictionary
        try:
            update_packet.messages = messages[register.username]
        # If the username doesn't exist in the messages, add the user
        # to the messages dictionary and make it contain an empty dictionary
        except KeyError:
            messages[register.username] = {}
            # Add all of the messages addressed to the user to the update packet
            update_packet.messages = messages[register.username]
        # Send the update packet
        c.send(update_packet.encode_packet())
        # Receive an incoming packet from the user
        msg = TCPPacket.decode_packet(c.recv(1024))
        # If the packet isn't an empty packet,
        if not isinstance(msg, TCPPacket.EmptyPacket):
            # Try to add the message from the packet to the recipient's messages dictionary
            try:
                # This is a dictionary inside of a dictionary in order to have a recipient
                # and different senders to that recipient, each containing their own list
                # of messages
                messages[msg.recipient][msg.username].append(msg.message_bytes)
            # If there is a recipient or user not added, add them and initialize it to a blank list
            # and then add the message to the list
            except KeyError:
                messages[msg.recipient][msg.username] = []
                messages[msg.recipient][msg.username].append(msg.message_bytes)
        # Terminate the connection with the user
        c.close()


if __name__ == "__main__":
    main()
