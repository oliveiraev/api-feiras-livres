# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
# pylint: disable=invalid-name
"""
Hooks do behave.

https://pythonhosted.org/behave/tutorial.html#environmental-controls
"""


import behave.step_registry


step = behave.step_registry.registry.make_decorator("step")
given = behave.step_registry.registry.make_decorator("given")
when = behave.step_registry.registry.make_decorator("when")
then = behave.step_registry.registry.make_decorator("then")
