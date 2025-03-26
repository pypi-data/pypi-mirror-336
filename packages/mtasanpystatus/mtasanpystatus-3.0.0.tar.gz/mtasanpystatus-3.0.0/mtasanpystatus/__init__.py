import socket
from typing import Optional, List, Tuple

class ServerException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

# Module-level attributes
address: Optional[str] = None
name: Optional[str] = None
game: Optional[str] = None
port: Optional[int] = None
gamemode: Optional[str] = None
map: Optional[str] = None
version: Optional[str] = None
somewhat: Optional[str] = None
players: Optional[int] = None
maxplayers: Optional[int] = None
playing_now_names: Optional[List[str]] = None
join_link: Optional[str] = None

def _validate_address(addr: str) -> bool:
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False

def _read_row(response: bytes, start: int) -> Tuple[int, str]:
    if start >= len(response):
        raise ServerException("Unexpected end of server response.")

    length_byte = response[start:start + 1]
    if not length_byte:
        raise ServerException("Received empty length byte in response.")

    length = ord(length_byte) - 1
    if length < 0 or start + 1 + length > len(response):
        raise ServerException(f"Invalid length byte at index {start}, length: {length}")

    value = response[start + 1:start + 1 + length]
    return start + 1 + length, value.decode('utf-8', errors='ignore')

def _read_socket_data(response: bytes, addr: str, port_num: int):
    global address, name, game, port, gamemode, map, version, somewhat, players, maxplayers, playing_now_names, join_link
    
    # Store the connection address and port
    address = addr
    port = port_num
    
    start = 4
    params = ('game', 'port', 'name', 'gamemode', 'map', 'version', 'somewhat', 'players', 'maxplayers')
    values = {}
    
    for param in params:
        try:
            start, value = _read_row(response, start)
            values[param] = value
        except ServerException as e:
            print(f"Warning: Failed to parse {param}. Error: {str(e)}")
            values[param] = None

    # Skip unwanted fields
    for _ in range(3):
        try:
            if start >= len(response):
                raise ServerException("Unexpected end of response while skipping metadata.")
            start, _ = _read_row(response, start)
        except ServerException as e:
            print(f"Warning: Failed to skip metadata at index {start}. Error: {str(e)}")
            break

    # Parse player names
    playing_now_names = []
    try:
        num_players = int(values['players']) if values['players'] else 0
    except (TypeError, ValueError):
        print("Warning: Invalid player count in server response.")
        num_players = 0

    INVALID_NAMES = {"Website", "N/A"}

    for _ in range(num_players):
        try:
            start, player_name = _read_row(response, start)
            player_name = ''.join(char for char in player_name if char.isprintable() and ord(char) < 128)
            player_names = [name.strip() for name in player_name.split("?") if name.strip()]
            filtered_names = [name for name in player_names if name not in INVALID_NAMES and len(name) > 1]
            playing_now_names.extend(filtered_names)
        except ServerException as e:
            print(f"Warning: Failed to parse player names. Error: {str(e)}")
            break

    # Update all module attributes
    game = values['game']
    name = values['name']
    gamemode = values['gamemode']
    map = values['map']
    version = values['version']
    somewhat = values['somewhat']
    players = values['players']
    maxplayers = values['maxplayers']
    join_link = f'mtasa://{address}:{port}' if address and port else None

def connect(addr: str, port_num: int = 22003, timeout: float = 0.2):
    """Connect to a MTA:SA server and populate module attributes"""
    global address, port
    
    if not _validate_address(addr):
        raise ServerException(f'Invalid server address: {addr}')

    ase_port = port_num + 123
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    
    try:
        sock.connect((addr, ase_port))
        sock.send(b"s")
        response = sock.recv(16384)
        _read_socket_data(response, addr, port_num)
    except socket.error as e:
        raise ServerException(f"Can't connect to server. Original exception: {str(e)}")
    finally:
        sock.close()