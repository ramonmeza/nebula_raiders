import usocket as socket
import ustruct as struct


NTP_PACKET_SIZE: int = 48
UNIX_OFFSET = 2208988800


def get_server_time(hostname: str, port: int = 123) -> int:
    sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        addr_info = socket.getaddrinfo(hostname, port)[0][-1]
        req: bytearray = bytearray(NTP_PACKET_SIZE)
        req[0] = 0x23
        sock.sendto(bytes(req), addr_info)
        data, _ = sock.recvfrom(NTP_PACKET_SIZE)
    finally:
        sock.close()

    if len(data) != NTP_PACKET_SIZE:
        raise Exception(f"Invalid NTP response: {data}")

    tx_secs: int = struct.unpack(">I", data[40:44])[0]
    unix_time: int = tx_secs - UNIX_OFFSET
    return unix_time
