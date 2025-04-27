import socket
import threading
import json
from message import Message
from clock import LogicalClock

class Cliente:
    def __init__(self, nome, host='localhost', porta=5000):
        self.nome = nome
        self.relogio = LogicalClock()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, porta))
        self.socket.sendall((nome + '\n').encode())

        threading.Thread(target=self.ouvir).start()

    def enviar(self, conteudo, destino=None):
        self.relogio.increment()
        msg = Message(conteudo, self.nome, destino, self.relogio.get())
        self.socket.sendall((json.dumps(msg.to_dict()) + '\n').encode())

    def ouvir(self):
        while True:
            dados = self.socket.recv(4096)
            for linha in dados.decode().split('\n'):
                if not linha.strip():
                    continue
                entrada = json.loads(linha)
                msg = Message.from_dict(entrada)
                self.relogio.update(msg.timestamp)
                print(f"\n📩 {self.nome} recebeu de {msg.produtor}: '{msg.conteudo}' (TS local: {self.relogio.get()})")

if __name__ == "__main__":
    nome = input("Nome do cliente: ")
    cliente = Cliente(nome, host ="169.254.210.222")

    while True:
        destino = input("Destino (deixe vazio para broadcast): ").strip() or None
        conteudo = input("Mensagem: ")
        cliente.enviar(conteudo, destino)
