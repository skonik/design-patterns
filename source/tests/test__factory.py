import unittest
from creational.factory.abstract_factory import EktMetallProductFactory, UralMetallProductFactory


class TestAbstractFactory(unittest.TestCase):

    def setUp(self):
        self.urall_metall_docs = [
            ('трубы стальные d 1.2м дл.=6.5м', {'diameter': '1.2', 'length': '6.5'}),
            ('труба дл.=2м d 1', {'diameter': '1', 'length': '2'})
        ]

        self.ekt_metall_docs = [
            ('тр. 12x0.5x4', {'diameter': '12', 'thickness': '0.5', 'length': '4'}),
            ('тр. 5x1.5x6', {'diameter': '5', 'thickness': '1.5', 'length': '6'})
        ]

    def test_urall_metall_factory(self):
        for doc_line, answer in self.urall_metall_docs:
            product = UralMetallProductFactory.get_product(doc_line)
            self.assertIsNotNone(product)
            self.assertEqual(product.as_dict(), answer)

    def test_ekt_metall_factory(self):
        for doc_line, answer in self.ekt_metall_docs:
            product = EktMetallProductFactory.get_product(doc_line)
            self.assertIsNotNone(product)
            self.assertEqual(product.as_dict(), answer)
