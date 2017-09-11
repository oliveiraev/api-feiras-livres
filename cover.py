#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Executa os dois tipos de testes com cobertura."""


import sys
import unittest
import coverage
import behave.__main__


if __name__ == "__main__":
    COVER = coverage.Coverage()
    COVER.erase()
    COVER.start()
    if behave.__main__.main():
        sys.exit(1)
    COVER.stop()

    SUITE = unittest.TestLoader().discover(".", "*.py")
    COVER.start()
    if not unittest.TextTestRunner().run(SUITE).wasSuccessful():
        sys.exit(1)
    COVER.stop()

    sys.exit(int(COVER.report() < 70))
