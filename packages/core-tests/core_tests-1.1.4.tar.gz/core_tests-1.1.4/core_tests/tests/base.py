# -*- coding: utf-8 -*-

import os

from unittest import TestCase


class BaseTestCase(TestCase):
    """ Base class for Test Cases """

    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.resources_directory = f"{os.getcwd()}/tests/resources"
