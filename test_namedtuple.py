from collections import namedtuple
from unittest import TestCase

from addict import Dict


Empty = namedtuple('Empty', [])
Pair = namedtuple('Pair', ['name', 'data'])


class NamedTupleTest(TestCase):
    def test_empty_namedtuple(self):
        value = Dict(node=Empty())
        self.assertIsInstance(value.node, Empty)
        self.assertEqual(value.to_dict(), {'node': Empty()})

    def test_namedtuple_fields_are_hooked_and_unhooked(self):
        original = Pair('sample', {'answer': 42})
        value = Dict(node=original)
        self.assertIsInstance(value.node, Pair)
        self.assertIsInstance(value.node.data, Dict)
        self.assertEqual(value.node.data.answer, 42)
        plain = value.to_dict()
        self.assertIsInstance(plain['node'], Pair)
        self.assertIs(type(plain['node'].data), dict)
        self.assertEqual(plain['node'], original)
        self.assertIs(type(original.data), dict)

    def test_namedtuple_inside_list(self):
        value = Dict(nodes=[Empty(), Pair('sample', {'answer': 42})])
        self.assertIsInstance(value.nodes[0], Empty)
        self.assertIsInstance(value.nodes[1], Pair)
        self.assertEqual(value.nodes[1].data.answer, 42)

    def test_regular_sequences_keep_their_types(self):
        value = Dict(sequence=({'answer': 42},), empty=(), values=[1, 2])
        self.assertIsInstance(value.sequence, tuple)
        self.assertIsInstance(value.sequence[0], Dict)
        self.assertEqual(value.to_dict(), {
            'sequence': ({'answer': 42},), 'empty': (), 'values': [1, 2]})
