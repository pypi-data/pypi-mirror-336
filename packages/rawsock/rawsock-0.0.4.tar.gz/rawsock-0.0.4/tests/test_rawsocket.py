import pytest
import struct
from rawsock import RawSocket

@pytest.fixture
def raw_socket():
    return RawSocket("lo")  # Using loopback interface for testing

def test_parse_mac():
    assert RawSocket._parse_mac("00:11:22:33:44:55") == b"\x00\x11\x22\x33\x44\x55"

def test_parse_ip():
    assert RawSocket._parse_ip("192.168.1.1") == b"\xc0\xa8\x01\x01"

def test_invalid_mac():
    with pytest.raises(Exception, match="MAC address .* is not valid."):
        RawSocket._parse_mac("00:11:22:33:44")

def test_invalid_ip():
    with pytest.raises(Exception, match="IP address 999.999.999.999 is not valid."):
        RawSocket._parse_ip("999.999.999.999")

def test_frame():
    frame = RawSocket.frame("ff:ff:ff:ff:ff:ff", "00:11:22:33:44:55", payload="hello")
    assert len(frame) >= 64  # Ethernet frame min size
    assert frame[:6] == b"\xff\xff\xff\xff\xff\xff"  # Destination MAC
    assert frame[6:12] == b"\x00\x11\x22\x33\x44\x55"  # Source MAC
    assert frame[12:14] == b"\x88\xb5"  # Default ethertype

def test_frame_custom_ethertype():
    frame = RawSocket.frame("ff:ff:ff:ff:ff:ff", "00:11:22:33:44:55", ethertype=b"\x08\x00", payload="data")
    assert frame[12:14] == b"\x08\x00"  # IPv4 ethertype

def test_send_arp(raw_socket):
    result = raw_socket.send_arp(
        source_mac="00:11:22:33:44:55",
        source_ip="192.168.1.1",
        target_ip="192.168.1.2"
    )
    assert result == 1  # Assuming successful send

def test_send_arp_with_frame(raw_socket):
    frame = RawSocket.frame("ff:ff:ff:ff:ff:ff", "00:11:22:33:44:55", ethertype=b"\x08\x06", payload=b"ARP TEST")
    result = raw_socket.send_arp(frame=frame)
    assert result == 1

def test_send_arp_invalid_args(raw_socket):
    with pytest.raises(TypeError, match="Either a frame or other parameters must be provided!"):
        raw_socket.send_arp()

def test_open_bpf_device(raw_socket):
    try:
        raw_socket._open_bpf_device()
        assert raw_socket.bpf_device is not None
    except Exception as e:
        assert "No available BPF device found" in str(e)

def test_bind_bpf(raw_socket):
    try:
        raw_socket.bind_bpf()
        assert raw_socket.bpf_device is not None
    except Exception as e:
        assert "No available BPF device found" in str(e)

def test_listener_setup(raw_socket):
    listener = raw_socket.listener(timeout=3, filter_={"ethertype": b"\x08\x06"})
    assert listener is not None
    assert listener.timeout == 3
    assert listener.filter_ == {"ethertype": b"\x08\x06"}

def test_listener_packet_parsing():
    packet = b"\x01\x02\x03\x04\x05\x06" + b"\x11\x12\x13\x14\x15\x16" + b"\x08\x00" + b"PAYLOAD"
    parsed = RawSocket._BPFListener.parse_packet(packet)
    assert parsed["destination_mac"] == "01:02:03:04:05:06"
    assert parsed["source_mac"] == "11:12:13:14:15:16"
    assert parsed["ethertype"] == b"\x08\x00"
    assert parsed["payload"] == b"PAYLOAD"

def test_listener_packet_filtering():
    packet = b"\x01\x02\x03\x04\x05\x06" + b"\x11\x12\x13\x14\x15\x16" + b"\x08\x00" + b"FILTER_ME"
    parsed = RawSocket._BPFListener.parse_packet(packet, filter_={"payload": [b"FILTER_ME"]})
    assert parsed is not None

    parsed_fail = RawSocket._BPFListener.parse_packet(packet, filter_={"payload": [b"NOT_FOUND"]})
    assert parsed_fail is None

def test_bpf_listener_context_manager(raw_socket):
    listener = raw_socket.listener(timeout=2)
    with listener as sock:
        assert sock is not None
