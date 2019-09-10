"""
Let's assume that we have two excel docs that describe their product info in different forms.
We want to parse the info and that's why we create common factory and product interface with different product and factory realizations.
"""

import abc
import re


class AbstractProductFactory(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def get_product(cls, string):
        """ Override this method to provide specific product creation."""
        raise NotImplementedError


class Product(abc.ABC):

    def __init__(self, raw_data):
        self.raw_data = raw_data

    @abc.abstractmethod
    def as_dict(self):
        raise NotImplemented

    def __str__(self):
        return self.__repr__()


class UralMetallPipe(Product):
    name_pattern = re.compile(r'\bтруб[аы]\b', re.U + re.I)
    length_pattern = re.compile(
        r'дл\.?=(?P<length_value>\d+(?:[,.]\d+)?)',
        re.U + re.I
    )
    diameter_pattern = re.compile(r'\bd\s*(?P<diameter_value>\d+(?:[.,]\d+)?)', re.I)

    def as_dict(self):
        result_dict = {
            'length': '',
            'diameter': ''
        }

        length_pattern_search = self.length_pattern.search(self.raw_data)
        if length_pattern_search:
            result_dict.update(
                {'length': length_pattern_search.group('length_value')}
            )

        diameter_pattern_search = self.diameter_pattern.search(self.raw_data)
        if diameter_pattern_search:
            result_dict.update(
                {'diameter': diameter_pattern_search.group('diameter_value')}
            )

        return result_dict


class EktMetallPipe(Product):
    name_pattern = re.compile(r'\bтр\.', re.U + re.I)
    sizes_pattern = re.compile(
              r'(?P<diameter>\d+(?:[,.]\d+)?)[xх]'
              r'(?P<thickness>\d+(?:[,.]\d+)?)[хx]'
              r'(?P<length>\d+(?:[,.]\d+)?)',
              re.U + re.I
    )

    def as_dict(self):
        result_dict = {
            'diameter': '',
            'thickness': '',
            'length': ''
        }

        sizes_pattern_search = self.sizes_pattern.search(self.raw_data)
        if sizes_pattern_search:
            result_dict.update(
                {
                    'diameter': sizes_pattern_search.group('diameter'),
                    'thickness': sizes_pattern_search.group('thickness'),
                    'length': sizes_pattern_search.group('length')
                }
            )

        return result_dict


class BaseFactory(AbstractProductFactory):
    products = []

    @classmethod
    def get_product(cls, string):
        for product_klass in cls.products:
            if product_klass.name_pattern.search(string):
                return product_klass(string)

        return None


class UralMetallProductFactory(BaseFactory):
    products = [
        UralMetallPipe
    ]


class EktMetallProductFactory(BaseFactory):
    products = [
        EktMetallPipe
    ]


if __name__ == '__main__':
    urall_metall_docs = [
        'трубы стальные d 1.2м дл.=6.5м',
        'труба дл.=2м d 1',
    ]
    ural_metall_factory = UralMetallProductFactory()
    for doc_line in urall_metall_docs:
        product = UralMetallProductFactory.get_product(doc_line)
        if product:
            print(product.as_dict())

    # {'length': '6.5', 'diameter': '1.2'}
    # {'length': '2', 'diameter': '1'}

    ekt_metall_docs = [
        'тр. 12x0.5x4',
        'тр. 5x1.5x6'
    ]
    for doc_line in ekt_metall_docs:
        product = EktMetallProductFactory.get_product(doc_line)
        if product:
            print(product.as_dict())

    # {'diameter': '12', 'thickness': '0.5', 'length': '4'}
    # {'diameter': '5', 'thickness': '1.5', 'length': '6'}
