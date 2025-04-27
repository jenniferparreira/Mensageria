import socket
import threading
import json
from message import Message
from buffer import MessageBuffer
from logger import MessageLogger

clientes = {}  # nome: socket
canais = {}    # canal: [nomes]
buffer = MessageBuffer()
logger = MessageLogger()

def enviar_para_cliente(cliente_socket, mensagem):
    try:
        cliente_socket.sendall((json.dumps(mensagem.to_dict()) + '\n').encode())
    except:
        pass

def lidar_com_cliente(cliente_socket, endereco):
    nome = cliente_socket.recv(1024).decode().strip()
    clientes[nome] = cliente_socket
    print(f"[+] Cliente conectado: {nome} ({endereco})")

    while True:
        try:
            dados = cliente_socket.recv(4096)
            if not dados:
                break
            for linha in dados.decode().split('\n'):
                if not linha.strip():
                    continue
                entrada = json.loads(linha)
                msg = Message.from_dict(entrada)
                logger.registrar(msg.to_dict() | {"status": "RECEBIDA"})
                buffer.adicionar(msg)

                # Entregar diretamente
                if msg.consumidor:
                    if msg.consumidor in clientes:
                        enviar_para_cliente(clientes[msg.consumidor], msg)
                        logger.registrar(msg.to_dict() | {"status": "ENTREGUE"})

                # Broadcast
                elif msg.consumidor is None:
                    for nome_dest, sock in clientes.items():
                        if nome_dest != msg.produtor:
                            enviar_para_cliente(sock, msg)
                            logger.registrar(msg.to_dict() | {"status": "ENTREGUE"})

        except Exception as e:
            print(f"Erro com {nome}: {e}")
            break

    print(f"[-] Cliente desconectado: {nome}")
    clientes.pop(nome)
    cliente_socket.close()

def iniciar_servidor(host='0.0.0.0', porta=5000):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, porta))
    servidor.listen()
    print(f"🟢 Servidor iniciado em {host}:{porta}")

    while True:
        cliente_socket, endereco = servidor.accept()
        threading.Thread(target=lidar_com_cliente, args=(cliente_socket, endereco)).start()

if __name__ == "__main__":
    iniciar_servidor()
