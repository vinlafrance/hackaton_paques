import json
import socket

address = ('54.87.189.174', 1337)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
print(s.recv(2048).decode())

team = input('Pizza')
players = input('Vincent, Dany, Maxime, Clément').split(',')

data = {
	'method': 'register',
	'team_name': team,
	'participants': players
}

print(f'Registering team {team} with players: {players}')

m = json.dumps(data).encode() + b'\n'
s.sendall(m)
print(s.recv(2048).decode())