import unittest
from ..patent_lookup import Lookup

class LookupTest(unittest.TestCase):
    def test_patent_to_int(self):
        c = Lookup(6606639)
