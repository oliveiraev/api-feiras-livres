# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Passos referentes à manipulação do servidor web2py."""

import os
import re
import logging
import features.tools.server

from features.environment import before_all, before_scenario, after_all


@before_all
def silence_server_errors(unused_context):
    u"""Reduz os logs durantes os testes."""
    logger = logging.getLogger("werkzeug")
    logger.setLevel(logging.FATAL)


@before_all
def start_server(context):
    u"""Inicializa um único servidor para todo o conjunto."""
    context.server = features.tools.server.Server(server_name="behave")
    context.server.start()


@after_all
def stop_server(context):
    u"""Encerra o servidor inicializado."""
    context.server.stop()


@before_scenario
def cleanup_database(unused_context, unused_scenario):
    u"""Limpa o banco de dados antes de cada cenário."""
    project_root = features.tools.ROOT_DIR
    source_db = os.path.join(project_root, "fixtures", "test-database.sqlite")
    dest_db = re.match(r"^sqlite://(.*)$", os.environ.get("DSN")).group(1)
    open(dest_db, "wb+").write(open(source_db, "rb").read())
