from scapy.all import *
import pydivert
import socket

def sync(packet, localIP):
    srcaddr = packet.src_addr
    srcport = packet.src_port
    tcpHeaders = pydivert.packet.TCPHeader(packet)
    SeqNum = tcpHeaders.seq_num
    AckNum = tcpHeaders.seq_num + 1
    ip=IP(src=localIP, dst=srcaddr)
    SynAck=TCP(sport=1234, dport=srcport, flags="SA", seq=SeqNum, ack=AckNum, options=[('MSS', 1460)])
    Acknowledge=sr1(ip/SynAck)
    httpGet = pydivert.WinDivert("tcp.DstPort == 1234")
    httpGet.open()
    httpPacket = httpGet.recv()
    httpGet.send(httpPacket)
    httpGet.close()
    newtcpHeaders = pydivert.packet.TCPHeader(httpPacket)
    AckNum = AckNum + newtcpHeaders.seq_num
    SeqNum = tcpHeaders.seq_num + 1
    html = "HTTP/1.1 200 OK\x0d\x0aServer: Testserver\x0d\x0aConnection: Keep-Alive\x0d\x0aContent-Type: text/html; charset=UTF-8\x0d\x0aContent-Length: 291\x0d\x0a\x0d\x0a<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"><html><head><title>Server</title></head><body bgcolor=\"black\" text=\"white\" link=\"blue\" vlink=\"purple\" alink=\"red\"><p><font face=\"Courier\" color=\"blue\">-Server is running</font></p></body></html>"
    data = TCP(sport=1234, dport=srcport, flags="PA", seq=SeqNum, ack=AckNum, options=[('MSS', 1460)])
    ackdata = sr1(ip/data/html)
    SeqNum = ackdata.ack
    RST = TCP(sport=1234, dport=srcport, flags="RA", seq=SeqNum, ack=AckNum, options=[('MSS', 1460)])
    send(ip/RST)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
localIP = (s.getsockname()[0])
s.close()
with pydivert.WinDivert("tcp.DstPort == 1234") as syn:
    for packet in syn:
        syn.send(packet)
        sync(packet, localIP)
