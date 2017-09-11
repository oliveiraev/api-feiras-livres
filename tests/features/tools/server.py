# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Testa o servidor web2py do behave."""

import os
import socket
import unittest
import mock
import features.tools.server
import werkzeug.serving


os.environ.setdefault("DSN", "sqlite:memory:")
werkzeug.serving.BaseWSGIServer = mock.Mock(
    spec=werkzeug.serving.BaseWSGIServer,
    name="werkzeug.serving.BaseWSGIServer",
    side_effect=mock.Mock
)
socket.socket.bind = mock.Mock(spec=socket.socket.bind)


class Server(unittest.TestCase):
    u"""Servidor de teste."""

    test_server = None

    def setUp(self):
        u"""Nova instância de servidor para cada teste."""
        self.test_server = features.tools.server.Server()

    def test_port_lookup(self):
        u"""Teste de verificação de porta disponível."""
        port_before = self.test_server.options.get("port")
        socket.socket.bind.side_effect = [socket.error, None]
        self.test_server.start()
        socket.socket.bind.side_effect = None
        port_after = self.test_server.options.get("port")
        assert port_after == port_before + 1, (port_before, port_after)

    def test_server_start(self):
        u"""Teste de chamada ao inicializador do servidor pela thread."""
        self.test_server.start()
        self.test_server.instance.serve_forever.assert_called_once()

    def test_server_stop(self):
        u"""Teste de chamada ao encerramento do servidor pela thread."""
        assert self.test_server.instance.server_close.call_count is 0
        self.test_server.stop()
        assert self.test_server.instance.server_close.call_count is 0
        self.test_server.start()
        self.test_server.stop()
        assert self.test_server.instance.server_close.call_count is 1
        self.test_server.stop()
        assert self.test_server.instance.server_close.call_count == 2
