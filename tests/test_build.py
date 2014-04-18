#!/usr/bin/env python2.7

import unittest
import os
from mmrun import main


class EndToEndTests(unittest.TestCase):
    def test_end_to_end_simple(self):
        main(os.path.join(os.getcwd(),'tests/test_build.yaml'))

if __name__=="__main__":
    unittest.main()

