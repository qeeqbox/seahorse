__G__ = "(G)bd249ce4"

from scapy.all import *
from sys import stdout
from binascii import hexlify
from netifaces import ifaddresses, AF_INET, AF_LINK
from binascii import hexlify
from multiprocessing import Process
from re import search as rsearch
from re import compile as rcompile
from logging import DEBUG, basicConfig, getLogger
from logging.handlers import RotatingFileHandler
from datetime import datetime


class QSniffer():
    def __init__(self, filter=None, interface=None):
        self.current_ip = ifaddresses(interface)[AF_INET][0]['addr'].encode('utf-8')
        self.current_mac = ifaddresses(interface)[AF_LINK][0]['addr'].encode('utf-8')
        self.filter = filter
        self.interface = interface
        self.method = "ALL"
        self.ICMP_codes = [(0, 0, 'Echo/Ping reply'), (3, 0, 'Destination network unreachable'), (3, 1, 'Destination host unreachable'), (3, 2, 'Desination protocol unreachable'), (3, 3, 'Destination port unreachable'), (3, 4, 'Fragmentation required'), (3, 5, 'Source route failed'), (3, 6, 'Destination network unknown'), (3, 7, 'Destination host unknown'), (3, 8, 'Source host isolated'), (3, 9, 'Network administratively prohibited'), (3, 10, 'Host administratively prohibited'), (3, 11, 'Network unreachable for TOS'), (3, 12, 'Host unreachable for TOS'), (3, 13, 'Communication administratively prohibited'), (3, 14, 'Host Precedence Violation'), (3, 15, 'Precendence cutoff in effect'), (4, 0, 'Source quench'),
                           (5, 0, 'Redirect Datagram for the Network'), (5, 1, 'Redirect Datagram for the Host'), (5, 2, 'Redirect Datagram for the TOS & network'), (5, 3, 'Redirect Datagram for the TOS & host'), (8, 0, 'Echo/Ping Request'), (9, 0, 'Router advertisement'), (10, 0, 'Router discovery/selection/solicitation'), (11, 0, 'TTL expired in transit'), (11, 1, 'Fragment reassembly time exceeded'), (12, 0, 'Pointer indicates the error'), (12, 1, 'Missing a required option'), (12, 2, 'Bad length'), (13, 0, 'Timestamp'), (14, 0, 'Timestamp Reply'), (15, 0, 'Information Request'), (16, 0, 'Information Reply'), (17, 0, 'Address Mask Request'), (18, 0, 'Address Mask Reply'), (30, 0, 'Information Request')]
        self.allowed_ports = []
        self.allowed_ips = []
        self.common = rcompile('pass|user|login')
        self.logs = getLogger("seahorse")
        self.logs.setLevel(DEBUG)
        basicConfig()

    def find_ICMP(self, x1, x2):
        for _ in self.ICMP_codes:
            if x1 == _[0] and x2 == _[1]:
                return _[2]
        return "None"

    def get_layers(self, packet):
        try:
            yield packet.name
            while packet.payload:
                packet = packet.payload
                yield packet.name
        except BaseException:
            pass

    def scapy_sniffer_main(self):
        _q_s = self

        def capture_logic(packet):
            _layers, hex_payloads, raw_payloads, _fields, _raw, _hex = [], {}, {}, {}, 'None', 'None'
            _layers = list(self.get_layers(packet))

            try:
                if _q_s.method == "ALL":
                    # only incoming packets - hmmmm
                    if packet.haslayer(Ether) and packet[Ether].dst == get_if_hwaddr(conf.iface).lower():
                        if packet[Ether].src != get_if_hwaddr(conf.iface).lower():
                            for layer in _layers:
                                try:
                                    _fields[layer] = packet[layer].fields
                                    if "load" in _fields[layer]:
                                        raw_payloads[layer] = _fields[layer]["load"]
                                        hex_payloads[layer] = hexlify(_fields[layer]["load"])
                                except Exception as e:
                                    pass
                            _q_s.logs.info([datetime.now().isoformat(), {'action': 'all', 'ip': _q_s.current_ip, 'mac': _q_s.current_mac, 'layers': _layers, 'fields': _fields, "payload": hex_payloads}])
            except Exception as e:
                pass

            stdout.flush()

        sniff(filter=self.filter, iface=self.interface, prn=capture_logic)


x = QSniffer('', 'eth0')
x.scapy_sniffer_main()
