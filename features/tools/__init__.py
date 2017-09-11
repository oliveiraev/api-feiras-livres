# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Ferramentas para execução dos testes de comportamento do behave."""


import os


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TEST_DATABASE = os.path.join(ROOT_DIR, "behave-database.sqlite")

os.environ.setdefault("PYTHONPATH", ROOT_DIR)
os.environ.setdefault("FLASK_APP", os.path.join(ROOT_DIR, "src"))
os.environ.setdefault("DSN", "sqlite:///{}".format(TEST_DATABASE))

# garante que o banco de testes exista para prevenir erros de leitura
open(TEST_DATABASE, "ab+")
