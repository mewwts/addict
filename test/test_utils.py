# Import built-in modules
import unittest

# Import third-party modules
from parameterized.parameterized import parameterized

# Import local modules
from addict import entity_addict

TEST_VAL = [1, 2, 3]
TEST_DICT = {'a': {'b': {'c': TEST_VAL}}}


class TestUtils(unittest.TestCase):
    @parameterized.expand(
        [
            ('test_1', TEST_DICT),
            ('test_2', [TEST_DICT]),
            ('test_3', [1, 1, TEST_DICT]),
            ('test_4', [1, 1, {'test': TEST_DICT}, 'a'])
        ]
    )
    def test_entity_addict(self, test_name, test_data):
        @entity_addict
        def hello_entity_addict():
            return test_data

        self.assertEqual(hello_entity_addict(), test_data)

if __name__ == '__main__':
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(verbosity=2)
    loaded_tests = loader.loadTestsFromTestCase(TestUtils)
    runner.run(loaded_tests)
