from websocket_server import WebsocketServer
import threading
import cherrypy
import queue

clientesConectados = {}

class ConectaCliente(threading.Thread):
    def __init__(self, cliente, servidor):
        threading.Thread.__init__(self)
        self.cliente = cliente
        self.conectado = True
        self.servidor = servidor
        self.mensagens = queue.Queue()

    def run(self):
        while self.conectado:
            try:
                mensagem = self.mensagens.get(block=True)
                if mensagem:
                    if ('username' not in self.cliente):
                        self.cliente['username'] = mensagem
                        self.servidor.send_message_to_all(f"{self.cliente['username']} entrou!")
                    else:
                        self.servidor.send_message_to_all(f"{self.cliente['username']}: {mensagem}")
            except Exception as erro:
                print(f"Cliente: {self.cliente['id']} Erro: {erro}")
                self.desconectaCliente()
        
    def mandaMsgPraFila(self, mensagem):
        self.mensagens.put(mensagem)
    
    def desconectaCliente(self):
        self.conectado = False

def novoCliente(cliente, servidor):
    print(f"Cliente conectado: {cliente['id']}")
    conectaCliente = ConectaCliente(cliente, servidor)
    clientesConectados[cliente['id']] = conectaCliente
    conectaCliente.start()

def novaMensagem(cliente, servidor, mensagem):
    conectaCliente = clientesConectados.get(cliente['id'])
    if (conectaCliente):
        conectaCliente.mandaMsgPraFila(mensagem)

def desconectaCliente(cliente, servidor):
    conectaCliente = clientesConectados.pop(cliente['id'], None)
    if conectaCliente:
        conectaCliente.desconectaCliente()
        servidor.send_message_to_all(f"{cliente['username']} saiu!")

class WebSocketServidor(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        servidor = WebsocketServer(port=15000, host='localhost')
        servidor.set_fn_new_client(novoCliente)
        servidor.set_fn_message_received(novaMensagem)
        servidor.set_fn_client_left(desconectaCliente)
        servidor.run_forever()

class Root:
    @cherrypy.expose
    def index(self):
        return "Servidor Webdocket iniciado"
    
if (__name__ == "__main__"):
    threadWebSocket = WebSocketServidor()
    threadWebSocket.start()
    cherrypy.quickstart(Root(), config={
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
        }
    })