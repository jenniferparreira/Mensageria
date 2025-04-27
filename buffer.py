class MessageBuffer:
    def __init__(self):
        self.buffer = []

    def adicionar(self, msg):
        self.buffer.append(msg)

    def obter_para(self, consumidor):
        msgs = [m for m in self.buffer if m.consumidor == consumidor or m.consumidor is None]
        self.buffer = [m for m in self.buffer if m not in msgs]
        return msgs
