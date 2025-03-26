# MTASANPyStatus

Multi Theft Auto San Andreas Server Monitoring Library

## Usage
Here are some key attributes you can access using mtasanpystatus:

| Attribute                     | Description                     | Example Value                     |
|-------------------------------|---------------------------------|-----------------------------------|
| `mtasanpystatus.address`      | Server IP address               | `'01.23.456.789'`                 |
| `mtasanpystatus.name`         | Server name                     | `'Ieoub MTA SERVER'`              |
| `mtasanpystatus.port`         | Server port                     | `22003`                           |
| `mtasanpystatus.game`         | Always "MTA:SA"                 | `'MTA:SA'`                        |
| `mtasanpystatus.gamemode`     | Current gamemode                | `'Freeroam'`                      |
| `mtasanpystatus.map`          | Current map                     | `'Los Santos'`                    |
| `mtasanpystatus.version`      | Server version                  | `'1.6'`                           |
| `mtasanpystatus.players`      | Online players count            | `5`                              |
| `mtasanpystatus.maxplayers`   | Max player slots                | `32`                             |
| `mtasanpystatus.join_link`    | Direct join link                | `'mtasa://01.23.456.789:22003'`   |
| `mtasanpystatus.playing_now_names` | List of player names [not recommended]       | `['Player1', 'Player2']`          |



## Installation

Install the library [using pip](https://pypi.org/project/mtasanpystatus/):

```bash
pip install mtasanpystatus
