import os
import struct
import fcntl
import threading

class RawSocket:

    BPF_DEVICES_COUNT = 4
    BIOCSETIF = 0x8020426c  # Set interface for BPF
    BIOCIMMEDIATE = 0x80044270  # immediate mode for BPF
    
    def __init__(self, ifname):
        if not isinstance(ifname, bytes):
            ifname = bytes(ifname.encode())
        self.ifname = ifname
        self._bpf_listener = None

    def send(self, frame: bytes):
        # open a bpf device and bind it to network card
        if (self._bpf_listener and not self._bpf_listener.running) or self._bpf_listener is None:
            self.bind_bpf()
        # write the frame to the bound BPF device
        try:
            os.write(self.bpf_device, frame)
        except OSError as e:
            print("Packet not sent!\n" + e)
            return 0
        finally:
            if self.bpf_device is not None and self._bpf_listener is None:
                try:
                    os.close(self.bpf_device)
                except OSError:
                    pass
        return 1

    def send_arp(
            self, *, frame: bytes = bytes(), source_mac: bytes | str = bytes(),
            source_ip: bytes | str = bytes(), target_ip: bytes | str = bytes()
        ):
        source_mac, source_ip, target_ip = (
            __class__._parse_mac(source_mac),
            __class__._parse_ip(source_ip),
            __class__._parse_ip(target_ip),
        )
        if not len(frame) and len(source_mac + source_ip + target_ip) != 14:
            raise TypeError("Either a frame or other parameters must be provided!")
        if len(frame):
            return self.send(frame)

        # ARP Header Fields
        hw_type = b'\x00\x01'  # Ethernet = 1
        proto_type = b'\x08\x00'  # IPv4
        hw_length = b'\x06'
        proto_length = b'\x04'
        opcode = b'\x00\x01'  # 1 for Request or 2 for Reply
        arp_frame_header = (
            hw_type + proto_type + hw_length + proto_length
            + opcode + source_mac + source_ip + b"\x00" * 6 + target_ip
        )
        frame = RawSocket.frame(b"\xff" * 6, source_mac, ethertype=b"\x08\x06", payload=arp_frame_header) # 0x0806 -> ARP
        return self.send(frame)

    def _open_bpf_device(self):
        for i in range(RawSocket.BPF_DEVICES_COUNT):
            try:
                self.bpf_device = os.open(f"/dev/bpf{i}", os.O_RDWR)
                break
            except FileNotFoundError:
                continue
        if self.bpf_device is None:
            raise Exception("No available BPF device found")

    @staticmethod
    def frame(
        dest_mac: bytes | str, source_mac: bytes | str, *, ethertype: bytes = b'\x88\xB5', payload: str | bytes = bytes()
    ):
        dest_mac, source_mac = (
            __class__._parse_mac(dest_mac),
            __class__._parse_mac(source_mac),
        )
        if not isinstance(payload, bytes):
            payload = bytes(payload.encode("utf-8"))
        payload_length = len(payload)
        if payload_length < 46:
            # pad payload with zeros to ensure its at least 46 bytes for ethernet packets (layer 2)
            payload = struct.pack(f"{46 if payload_length < 46 else payload_length}s", payload)
        return dest_mac + source_mac +  ethertype + payload # FCS (4 bytes) gets added automatically by the network interface

    def bind_bpf(self):
        self._open_bpf_device()
        ifr = struct.pack("16s", self.ifname) # network interface must be 16 bytes
        # Bind the BPF device to the specified network interface
        fcntl.ioctl(self.bpf_device, RawSocket.BIOCSETIF, ifr)
        # enable immdeiate mode
        self._set_bpf()
    
    def _set_bpf(self):
        immediate_mode = struct.pack("I", 1)
        # enabling BIOCIMMEDIATE ensures packets are processed and sent immediately
        # to ensure packets don't get stuck in buffer.
        fcntl.ioctl(self.bpf_device, RawSocket.BIOCIMMEDIATE, immediate_mode)
    
    def listener(self, timeout: int, *, filter_: str | None = None):
        listener = self._BPFListener(self, buffer_size=4096)
        listener.filter_ = filter_
        listener.timeout = timeout
        self._bpf_listener = listener
        return listener
    
    @staticmethod
    def _parse_ip(ip: str) -> bytes:
        if isinstance(ip, bytes):
            return ip
        decimals = ip.strip().split(".")
        try:
            raw_ip = b"".join([int(dec).to_bytes(1, 'big') for dec in decimals])
        except OverflowError: # ip exceeds 4 bytes
            raise Exception(f"IP address {ip} is not valid.")
        return raw_ip

    @staticmethod
    def _parse_mac(mac: str) -> bytes:
        if isinstance(mac, bytes):
            return mac
        hex_values = mac.strip().split(":")
        try:
            raw_mac = b"".join([bytes.fromhex(val) for val in hex_values])
        except ValueError:
            raise Exception(f"MAC address {mac} is not valid.")
        if len(raw_mac) != 6:
            raise Exception(f"MAC address {mac} is not valid.")
        return raw_mac

    class _BPFListener:
        def __init__(self, raw_socket: "RawSocket", buffer_size=4096):
            if not isinstance(raw_socket, RawSocket):
                raise ValueError(f"{raw_socket} is not an object of RawSocket.")
            self.socket = raw_socket
            self.device = None
            self.buffer_size = buffer_size
            self.packets = []
            self.running = False
            self.thread = None
            self.timeout = 5
            self.filter_ = None

        def __getattribute__(self, name):
            attr = object.__getattribute__(self, name)
            if callable(attr) and not self.in_context:
                raise RuntimeError(f"{self.__class__.__name__} is intended to be run as a context manager.")
            return attr

        def _capture_packets(self):
            if not self.running:
                self.socket.bpf_device = os.open(self.device, os.O_RDONLY)  # read-only
                self.running = True
            try:
                while self.running:
                    packet = os.read(self.socket.bpf_device, self.buffer_size)
                    packet = __class__.parse_packet(packet, self.filter_, True)
                    if packet is not None:
                        self.packets.append(packet)
            except OSError as e:
                print(f"Error reading from {self.device}: {e}")
            finally:
                os.close(self.socket.bpf_device)
        
        @staticmethod
        def parse_packet(packet, filter_: dict = dict(), bpf_header=False):
            if bpf_header:
                packet = packet[18:]
            packet = {
                "destination_mac": ":".join(f"{b:02x}" for b in packet[0:6]),
                "source_mac": ":".join(f"{b:02x}" for b in packet[6:12]),
                "ethertype": packet[12:14],
                "payload": packet[14:],
            }
            if filter_ is None:
                return packet
            for i in filter_.keys():
                if i == "payload" and isinstance(filter_[i], list):
                    for chunk in filter_["payload"]:
                        if chunk not in packet["payload"]:
                            return None
                elif i in packet and filter_[i] != packet[i]:
                    return None
            return packet

        def stop(self):
            self.running = False
            if self.thread:
                self.thread.join()

        def __enter__(self):
            self.socket.bind_bpf()
            self.in_context, self.running = True, True
            if self.thread is None or not self.thread.is_alive():
                self.thread = threading.Thread(target=self._capture_packets, daemon=True)
                self.thread.start()
            threading.Timer(self.timeout, self.stop).start()
            return self.socket

        def __exit__(self, exc_type, exc_value, traceback):
            event = threading.Event()
            try:
                event.wait(self.timeout)
            except KeyboardInterrupt:
                self.stop()
            self.socket.captured_packets = self.packets
            self.packets = []
            return False