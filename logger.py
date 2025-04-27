class MessageLogger:
    def __init__(self, arquivo='log.txt'):
        self.arquivo = open(arquivo, 'a')

    def registrar(self, linha):
        self.arquivo.write(linha + '\n')
        self.arquivo.flush()

    def __del__(self):
        self.arquivo.close()
