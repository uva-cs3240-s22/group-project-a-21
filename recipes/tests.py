from django.test import TestCase

# Create your tests here.

class DummyTests(TestCase):

    # MUST begin with test.
    def test_dummy(self):
        """
        dummy test, asserts true    
        """
        self.assertTrue(True)

