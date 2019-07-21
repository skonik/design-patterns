

class SingletonMeta(type):
    instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(*args, **kwargs)
        return cls.instances[cls]


class SingleWithMeta(metaclass=SingletonMeta):
    pass


class Singleton:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance


if __name__ == '__main__':
    # Simple singleton.
    singleton1 = Singleton()
    singleton2 = Singleton()
    print(singleton1 is singleton2)  # True

    # SingletonMeta.
    singleton_meta1 = SingleWithMeta()
    singleton_meta2 = SingleWithMeta()
    print(singleton_meta1 is singleton_meta2)  # True
