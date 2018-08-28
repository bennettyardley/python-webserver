# python-webserver

## Server.py
The main web server script. Works by waiting for a SYN packet from a client over port 1234 and responding with a SYN-ACK packet. Once communication has been established (3 Way Handshake) an HTTP packet containing HTML is sent to the client and communication is ended by the server with an RST packet.

## Requirements 
* [pydivert](https://github.com/ffalcinelli/pydivert)
* [Scapy](https://github.com/secdev/scapy)
* Written in [Python 3.7](https://www.python.org/downloads/release/python-370/)

## Todo
* Get Destination address from the SYN packet instead of the localIP variable.
* Multi-threading for multiple connections at the same time
* Fix other bugs
