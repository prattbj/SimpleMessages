# Created by Benjamin Pratt on 11/8/2022
import socket
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import TCPPacket


def main():
    """
    Run the client. Allows the client to send and receive end-to-end encrypted messages.
    """
    # Port number we are using
    port = 5000

    # Tries to open files that have our username and keys stored
    try:
        with open("user.txt", 'r') as u:
            user = u.read()
        with open("private.key", 'rb') as b:
            private_key = b.read()
        with open("public.key", 'rb') as b:
            public_key = b.read()

        key = crypto_serialization.load_pem_private_key(private_key, None, crypto_default_backend())
    # If it can't find the files, it will generate a new public and private key as well as
    # ask for a username
    except FileNotFoundError:
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )

        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption()
        )

        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
        )

        with open('private.key', 'wb') as f:
            f.write(private_key)
        with open('public.key', 'wb') as f:
            f.write(public_key)
        with open('user.txt', 'w') as f:
            user = input("Enter a username: ")
            f.write(user)

    # Loop to allow the user to send and receive messages
    is_running = True
    while is_running:
        # Connect to the server
        s = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM)

        s.connect(('127.0.0.1', port))

        # Send a RegisterPacket so the server knows who you are
        s.send(TCPPacket.RegisterPacket(user, public_key).encode_packet())

        # Server returns a packet containing a dictionary of users and a dictionary of messages
        update = TCPPacket.decode_packet(s.recv(1024))
        users, messages = update.users, update.messages

        # Print the names of people that have sent you messages
        print("You have messages from: ")
        for name in messages.keys():
            print(f"\t{name}")

        # Read messages
        while True:
            name = input("Type the name of the user you would like to read the message of, or type 'no' to stop. ")
            if name == 'no':
                break
            for msg in messages[name]:
                # Decrypt the message
                decrypted = key.decrypt(msg, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                          algorithm=hashes.SHA256(), label=None))
                # Display the message
                print(f"\t{decrypted.decode('utf-8')}")

        # Allow the user to send a message
        name = input("Type the name of the user you would like to send a message to, or type 'no'. ")
        if name == 'no':
            # If the user doesn't want to send a message, send a blank packet so that the server closes
            # the connection with the user and doesn't error out waiting for a message
            s.send(TCPPacket.EmptyPacket().encode_packet())
        else:
            # Get the public key of the user you want to send a message to
            p_key = crypto_serialization.load_ssh_public_key(users[name])
            # Send the encrypted message to the server
            s.send(TCPPacket.TextPacket(user, name, p_key.encrypt(bytes(input("Enter your message: "), 'utf-8'),
                                        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                     algorithm=hashes.SHA256(),
                                                     label=None))).encode_packet())
        is_running = not (input("Would you like to continue sending and reading messages? (yes/no) ") == "no")


if __name__ == '__main__':
    main()

