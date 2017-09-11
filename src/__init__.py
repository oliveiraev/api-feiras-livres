# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Módulo de acesso à instância da aplicação."""


from src.application import app  # noqa: F401


__import__("src.controllers", fromlist=["*"])
