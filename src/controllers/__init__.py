# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""
Pacote dos controllers da aplicação.

Para um melhor entendimento das rotas, organize os controllers de acordo com o
caminho da URL, ex:

/something/another_thing deve ser colocado no controller something.py, e ser
roteado por um método preferivelmente nomeado another_thing
"""

from src.controllers import erros, feiras  # noqa: F401
