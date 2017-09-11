# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""
Execução da aplicação em ambiente de desenvolvimento.

Note que, de acordo com http://flask.pocoo.org/docs/0.12/server/#in-code,
invocar a aplicação desta maneira implica em desativação do auto-reloader.
"""


try:
    # Para execução com 'python src'
    from __init__ import app
except ImportError:
    # Para execução com 'python -m src'
    from src import app


if __name__ == "__main__":
    app.run()
