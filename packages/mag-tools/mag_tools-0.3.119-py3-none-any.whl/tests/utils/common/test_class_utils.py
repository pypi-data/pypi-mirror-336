import unittest
from typing import Optional

from utils.common.class_utils import ClassUtils


class TestClassUtils(unittest.TestCase):
    def test_get_optional_type(self):
        print(ClassUtils.get_optional_type(Optional[str]))
        print(ClassUtils.get_optional_type(Optional[int]))