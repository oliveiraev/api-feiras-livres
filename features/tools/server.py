# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
"""Manipula o servidor flask programaticamente."""

import sys
import socket
import threading
import time
import werkzeug.serving
from src import app


class Thread(threading.Thread):
    u"""Classe thread com métodos adicionais."""

    @property
    def started(self):
        u"""Verifica se a thread foi iniciada."""
        return getattr(self, "_started").is_set()

    @property
    def running(self):
        u"""Verifica se a thread ainda está em execução."""
        return self.started and self.is_alive()

    @property
    def stop(self):
        u"""Retorna o método de encerramento da thread."""
        return getattr(self, "_stop", lambda: None)


class Server(object):
    u"""Servidor flask."""

    options = {
        "listen": "127.0.0.1",
        "port": 8000
    }

    def __init__(self, port=8000, **params):
        u"""Inicializa o objeto com as opções recebidas."""
        self.options = dict(Server.options, **dict(port=port))
        self.options.update(params)
        self._instance = None
        self._thread = None

    @property
    def instance(self):
        u"""Garante que exista apenas uma instância do servidor por objeto."""
        if self._instance is not None:
            return self._instance
        self.options["port"] = int(self.options.get("port") or 1024)
        while not self._is_free_port(self.options.get("port")):
            self.options["port"] = self.options["port"] + 1
        self._instance = werkzeug.serving.BaseWSGIServer(
            host="127.0.0.1",
            port=self.options.get("port") or 65535,
            app=app
        )
        return self.instance

    @staticmethod
    def _is_free_port(port):
        is_free = True
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", port))
        except socket.error:
            is_free = False
        finally:
            sock.close()
        return is_free

    @property
    def thread(self):
        u"""Garante que exista apenas uma thread por instância."""
        if self._thread is not None:
            return self._thread
        self._thread = Thread(target=self.instance.serve_forever)
        return self.thread

    def start(self):
        u"""Inicializa o servidor."""
        self.thread.daemon = True
        self.run()

    def run(self):
        u"""Executa o servidor."""
        self.thread.start()

    def stop(self):
        u"""Encerra o servidor."""
        if not self.thread.started:
            return
        self.instance.shutdown()
        if self.thread.running:
            self.thread.join()

    __del__ = stop


if __name__ == "__main__":
    SERVER = Server(*sys.argv[1:])
    SERVER.start()
    while True:
        try:
            time.sleep(0.005)
        except KeyboardInterrupt:
            break
    print("Encerrando...")
    SERVER.stop()
