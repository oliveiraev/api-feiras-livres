# -*- coding: utf-8 -*-
# vim: sta sts=4 sw=4 et ai si ff=unix eol fenc=utf-8 nobomb ft=python
# pylint: disable=invalid-name
"""
Hooks do behave.

https://pythonhosted.org/behave/tutorial.html#environmental-controls
"""


import behave.step_registry
import features.tools.hook


step = behave.step_registry.registry.make_decorator("step")
given = behave.step_registry.registry.make_decorator("given")
when = behave.step_registry.registry.make_decorator("when")
then = behave.step_registry.registry.make_decorator("then")

before_all = features.tools.hook.BEFORE_ALL
before_tag = features.tools.hook.BEFORE_TAG
before_feature = features.tools.hook.BEFORE_FEATURE
before_scenario = features.tools.hook.BEFORE_SCENARIO
before_step = features.tools.hook.BEFORE_STEP

after_all = features.tools.hook.AFTER_ALL
after_tag = features.tools.hook.AFTER_TAG
after_feature = features.tools.hook.AFTER_FEATURE
after_scenario = features.tools.hook.AFTER_SCENARIO
after_step = features.tools.hook.AFTER_STEP
