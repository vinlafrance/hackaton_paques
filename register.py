import json
import socket

address = ('3.226.47.73', 1337)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
print(s.recv(2048).decode())

team = input('Insert team name: ')
players = input('Insert player names (separated by commas): ').split(',')

data = {
	'method': 'register',
	'team_name': team,
	'participants': players
}

print(f'Registering team {team} with players: {players}')

m = json.dumps(data).encode() + b'\n'
s.sendall(m)
print(s.recv(2048).decode())