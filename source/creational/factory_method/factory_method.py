import abc
import re


class Product(abc.ABC):

    def __init__(self, raw_data):
        self.raw_data = raw_data

    @abc.abstractmethod
    def as_dict(self):
        raise NotImplemented

    def __repr__(self):
        return self.__str__()


class Pipe(Product):
    """
    >> print(Pipe('pipe steel grade 120x1.5x6000')
    <Pipe diameter=120, thickness=1.5, length=6000>
    """
    name_pattern = re.compile(r'(?P<name>pipe)')
    sizes_pattern = re.compile(
              r'(?P<diameter>\d+(?:[,.]\d+)?)x' \
              r'(?P<thickness>\d+(?:[,.]\d+)?)x' \
              r'(?P<length>\d+(?:[,.]\d+)?)',
              re.U + re.I
    )

    def __init__(self, raw_data):
        super().__init__(raw_data)
        self.diameter = ''
        self.thickness = ''
        self.length = ''
        self.__parse_to_attributes(self.raw_data)

    def __parse_to_attributes(self, raw_data):
        size_pattern_search = self.sizes_pattern.search(raw_data)
        if size_pattern_search:
            self.diameter = size_pattern_search.group('diameter')
            self.thickness = size_pattern_search.group('thickness')
            self.length = size_pattern_search.group('length')

    def as_dict(self):
        return {
            'diameter': self.diameter,
            'thickness': self.thickness,
            'length': self.length
        }

    def __str__(self):
        return '<Pipe diameter={}, thickness={}, length={}>'.format(
            self.diameter,
            self.thickness,
            self.length
        )


class Sheet(Product):
    """
    >> print(Sheet('sheet 1.5x200x8000'))
    <Sheet height=1.5, width=200, length=8000>
    """
    name_pattern = re.compile('(?P<name>sheet)', re.U + re.I)
    sizes_pattern = re.compile(
              r'(?P<height>\d+(?:[,.]\d+)?)x' \
              r'(?P<width>\d+(?:[,.]\d+)?)x' \
              r'(?P<length>\d+(?:[,.]\d+)?)',
              re.U + re.I
    )

    def __init__(self, raw_data):
        super().__init__(raw_data)
        self.height = ''
        self.width = ''
        self.length = ''
        self.__parse_to_attributes(self.raw_data)

    def __parse_to_attributes(self, raw_data):
        sizes_pattern_search = self.sizes_pattern.search(raw_data)
        if sizes_pattern_search:
            self.height = sizes_pattern_search.group('height')
            self.width = sizes_pattern_search.group('width')
            self.length = sizes_pattern_search.group('length')

    def as_dict(self):
        return {
            'height': self.height,
            'width': self.width,
            'length': self.length
        }

    def __str__(self):
        return '<Sheet height={}, width={}, length={}>'.format(
            self.height,
            self.width,
            self.length
        )


class ProductCreator:
    registred_products = [
        Pipe,
        Sheet
    ]

    @classmethod
    def create_product(cls, raw_data):
        for registred_product in cls.registred_products:
            if registred_product.name_pattern.search(raw_data):
                return registred_product(raw_data)

        return None


if __name__ == '__main__':
    table_data = [
        'pipe steel grade 120x1.5x6000',
        'pipe no sizes',
        'sheet 1.5x200x8000'
    ]

    for raw_data in table_data:
        product = ProductCreator.create_product(raw_data)
        if product:
            print(product)
    # <Pipe diameter=120, thickness=1.5, length=6000>
    # <Pipe diameter=, thickness=, length=>
    # <Sheet height=1.5, width=200, length=8000>
