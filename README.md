# python-webserver

Requires pydivert and scapy. The server works by waiting for a SYN packet from a client and responding with a SYN-ACK packet. Once communication has been established an HTTP packet containing HTML is sent to the client and communication is ended by the server with an RST packet.
