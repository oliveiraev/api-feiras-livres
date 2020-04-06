#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
u"""Configuração do setuptools."""


import os
import sys
import shlex
import subprocess
import unittest
from setuptools import find_packages
from setuptools import setup
from setuptools.command.test import test as TestCommand


def run_unittest():
    u"""Especifica a execução de testes pelo setuptools via unittest."""
    return unittest.TestLoader().discover(".", pattern="*.py")


class BehaveTest(TestCommand):
    u"""Corrige a execução do behave pelo setup.py."""

    user_options = [('behave-args=', 'b', 'Arguments to pass to behave')]

    behave_command = None

    behave_args = []

    def initialize_options(self):
        u"""Inicializador e configuração."""
        TestCommand.initialize_options(self)
        self.behave_args = []
        # import here, cause outside the egg is not loaded
        from setuptools_behave import behave_test

        class _BehaveTest(behave_test):
            u"""Subclasse. Utilizada na execução do teste."""

            def behave(self, path):
                u"""Método principal."""
                behave = os.path.join("bin", "behave")
                if not os.path.exists(behave):
                    behave = "-m behave"
                cmd_options = self.distribution.command_options[
                    'behave_test'].get('behave_args', ['', ''])[1]
                self.announce("CMDLINE: python %s %s" % (behave, cmd_options),
                              level=3)
                behave_cmd = shlex.split(behave)
                return subprocess.call(
                    [sys.executable] + behave_cmd + shlex.split(cmd_options))
        self.behave_command = _BehaveTest(self.distribution)

    def finalize_options(self):
        u"""'TearDown' da classe."""
        self.behave_command.finalize_options()

    def run(self):
        u"""Executa os testes."""
        self.behave_command.run()


INSTALL_REQUIRES = [
    "Flask==1.1.2",
    "Flask-SQLAlchemy==2.2",
    "Flask-Validator==1.2.3",
    "mysql-connector-python==2.1.7",
]


TESTS_REQUIRE = [
    "behave==1.2.5",
    "coverage==4.4.1",
    "flake8==3.4.1",
    "mock==2.0.0",
    "pylint==1.7.2",
    "requests==2.20.0",
]


if __name__ == "__main__":
    setup(
        name="feiras-sp",
        version="0.0.1a0",
        author="Evandro Oliveira",
        author_email="evandrofranco@gmail.com",
        python_requires='>=3.2',
        install_requires=INSTALL_REQUIRES,
        tests_require=TESTS_REQUIRE,
        packages=find_packages(exclude=["features", "tests"]),
        include_package_data=True,
        test_suite="setup.run_unittest",
        cmdclass=dict(
            behave_test=BehaveTest
        )
    )
