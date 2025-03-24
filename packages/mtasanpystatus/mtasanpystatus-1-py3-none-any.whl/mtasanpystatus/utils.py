import socket

def validate_address(address: str) -> bool:
    """
    Validate the server address.

    :param address: The server IP address.
    :return: True if the address is valid, False otherwise.
    """
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False