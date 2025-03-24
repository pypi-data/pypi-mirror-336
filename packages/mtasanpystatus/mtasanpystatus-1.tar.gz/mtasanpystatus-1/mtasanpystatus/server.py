import socket
from typing import Optional, Tuple, List
from .exceptions import ServerException
from .utils import validate_address

class Server:
    timeout: float = 0.2
    game: Optional[str] = None
    port: Optional[int] = None
    name: Optional[str] = None
    gamemode: Optional[str] = None
    map: Optional[str] = None
    version: Optional[str] = None
    somewhat: Optional[str] = None
    players: Optional[int] = None
    maxplayers: Optional[int] = None
    playing_now_names: Optional[List[str]] = None  # New attribute for player names

    def __init__(self, address: str, port: int = 22003, **kwargs):
        if not validate_address(address):
            raise ServerException(f'Invalid server address: {address}')
        self.address = address
        self.port = port
        self.ase_port = port + 123
        self.__dict__.update(kwargs)
        self.response = None
        self.connect()
        self.read_socket_data()

    @property
    def join_link(self) -> str:
        return f'mtasa://{self.address}:{self.port}'

    @property
    def socket_addr(self) -> Tuple[str, int]:
        return self.address, self.ase_port

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)
        try:
            sock.connect(self.socket_addr)
            sock.send(b"s")
            self.response = sock.recv(16384)
        except socket.error as e:
            raise ServerException(f"Can't connect to server. Original exception: {str(e)}")
        finally:
            sock.close()

    def read_row(self, start: int) -> Tuple[int, str]:
        if start >= len(self.response):
            raise ServerException("Unexpected end of server response.")

        length_byte = self.response[start:start + 1]
        if not length_byte:
            raise ServerException("Received empty length byte in response.")

        length = ord(length_byte) - 1  # Subtract 1 to exclude the length byte itself
        if length < 0 or start + 1 + length > len(self.response):
            raise ServerException(f"Invalid length byte at index {start}, length: {length}")

        value = self.response[start + 1:start + 1 + length]
        return start + 1 + length, value.decode('utf-8', errors='ignore')

    def read_socket_data(self):
        start = 4
        params = ('game', 'port', 'name', 'gamemode', 'map', 'version', 'somewhat', 'players', 'maxplayers')
        for param in params:
            try:
                start, value = self.read_row(start)
                setattr(self, param, value)
            except ServerException as e:
                print(f"Warning: Failed to parse {param}. Error: {str(e)}")
                setattr(self, param, None)
                return

        # Skip unwanted fields: Script Version, Author, Website
        for _ in range(3):  # Skip 3 rows (Script Version, Author, Website)
            try:
                if start >= len(self.response):
                    raise ServerException("Unexpected end of response while skipping metadata.")
                start, _ = self.read_row(start)
            except ServerException as e:
                print(f"Warning: Failed to skip metadata at index {start}. Error: {str(e)}")
                return

        # Parse player names
        self.playing_now_names = []
        try:
            num_players = int(self.players) if self.players else 0
        except (TypeError, ValueError):
            print("Warning: Invalid player count in server response.")
            num_players = 0

        INVALID_NAMES = {"Website", "N/A"}  # Filter out unwanted names

        for _ in range(num_players):  # Loop through the number of online players
            try:
                start, player_name = self.read_row(start)
                
                # Clean up player names (remove non-printable characters)
                player_name = ''.join(char for char in player_name if char.isprintable() and ord(char) < 128)
                
                # Split player names if concatenated with special characters (e.g., "@", "?")
                player_names = [name.strip() for name in player_name.split("?") if name.strip()]
                
                # Filter out invalid names
                filtered_names = [name for name in player_names if name not in INVALID_NAMES and len(name) > 1]
                
                self.playing_now_names.extend(filtered_names)
            except ServerException as e:
                print(f"Warning: Failed to parse player names. Error: {str(e)}")
                break

        if len(self.playing_now_names) != num_players:
            print(f"Warning: Expected {num_players} players but extracted {len(self.playing_now_names)}.")

    def to_dict(self) -> dict:
        return {
            'game': self.game,
            'port': self.port,
            'name': self.name,
            'gamemode': self.gamemode,
            'map': self.map,
            'version': self.version,
            'somewhat': self.somewhat,
            'players': self.players,
            'maxplayers': self.maxplayers,
            'playing_now_names': self.playing_now_names,  # Include player names
            'join_link': self.join_link
        }
