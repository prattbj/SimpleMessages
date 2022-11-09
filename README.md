# Overview

I wanted to add online services to a video game I was making. However, I had no idea what I was doing! 

To learn networking, I instead decided to make a simple end-to-end encrypted message server.


[Software Demo Video](https://youtu.be/gEQYA40X4GI)

# Network Communication

I used a Client/Server architecture to make this network.

I am using TCP port 5000.

The messages being sent are in bytes, but prior to becoming bytes they are in the format of a custom Packet class.
This way the server and client can communicate multiple types of data with each other all at once.

# Development Environment

I used JetBrains PyCharm in order to program this.

I used Python with the socket, cryptography, and pickle libraries. These allow me to create and connect to a server,
encrypt and decrypt data, and encode/decode objects with ease.

# Useful Websites

* [GeeksForGeeks](https://www.geeksforgeeks.org)
* [Python Socket Documentation](https://docs.python.org/3.6/library/socket.html)
* [Cryptography Library Documentation](https://cryptography.io/en/latest/)
# Future Work

* Allow more than one user to connect to the server at once
* Store message and public key data in files so that they aren't deleted from the server when it shuts down
* Make a more fluid connection between the user and the server so that the user can decide what they want to do
* Add a gui
