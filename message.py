import json
import uuid

class Message:
    def __init__(self, conteudo, produtor, consumidor=None, timestamp=0):
        self.id = str(uuid.uuid4())
        self.conteudo = conteudo
        self.produtor = produtor
        self.consumidor = consumidor
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'id': self.id,
            'conteudo': self.conteudo,
            'produtor': self.produtor,
            'consumidor': self.consumidor,
            'timestamp': self.timestamp
        }

    @staticmethod
    def from_dict(d):
        msg = Message(d['conteudo'], d['produtor'], d['consumidor'], d['timestamp'])
        msg.id = d['id']
        return msg
