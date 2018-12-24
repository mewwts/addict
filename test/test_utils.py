# Import built-in modules
import unittest

# Import local modules
from addict import Dict
from addict import entity_addict

TEST_VAL = [1, 2, 3]
TEST_DICT = {'a': {'b': {'c': TEST_VAL}}}


class TestUtils(unittest.TestCase):
    def test_entity_addict(self):
        @entity_addict
        def hello_entity_addict_a():
            return TEST_DICT

        @entity_addict
        def hello_entity_addict_b():
            return [TEST_DICT]

        self.assertTrue(isinstance(hello_entity_addict_a(), Dict))
        self.assertTrue(isinstance(hello_entity_addict_b()[0], Dict))


if __name__ == '__main__':
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(verbosity=2)
    loaded_tests = loader.loadTestsFromTestCase(TestUtils)
    runner.run(loaded_tests)
