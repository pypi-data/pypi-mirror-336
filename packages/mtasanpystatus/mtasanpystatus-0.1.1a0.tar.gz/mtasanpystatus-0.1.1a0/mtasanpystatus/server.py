import socket
from typing import Optional, Tuple, List

from .exceptions import ServerException

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
    online_players_names: Optional[List[str]] = None  # New attribute for player names

    def __init__(self, address: str, port: int = 22003, **kwargs):
        self.validate_address(address)
        self.address = address
        self.port = port
        self.ase_port = port + 123
        self.__dict__.update(kwargs)
        self.response = None
        self.connect()
        self.read_socket_data()

    @staticmethod
    def validate_address(address: str):
        try:
            socket.inet_aton(address)
        except socket.error as e:
            raise ServerException(f'Invalid server address. Original exception: {e.strerror}')

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
        start_end = start + 1
        length = ord(self.response[start:start_end]) - 1
        value = self.response[start_end:start_end + length]
        return start_end + length, value.decode('utf-8')

    def read_socket_data(self):
        start = 4
        params = ('game', 'port', 'name', 'gamemode', 'map', 'version', 'somewhat', 'players', 'maxplayers')
        for param in params:
            start, value = self.read_row(start)
            setattr(self, param, value)

        # Parse online player names
        self.online_players_names = []
        for _ in range(int(self.players)):  # Loop through the number of online players
            start, player_name = self.read_row(start)
            self.online_players_names.append(player_name)

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
            'online_players_names': self.online_players_names,
            'join_link': self.join_link
        }