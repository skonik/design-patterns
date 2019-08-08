import abc


class Observer(abc.ABC):

    @abc.abstractmethod
    def update(self, subject) -> None:
        raise NotImplementedError


class Subject(abc.ABC):

    @abc.abstractmethod
    def attach(self, observer: Observer) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def detach(self, observer: Observer) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def notify(self) -> None:
        raise NotImplementedError


class VkCallbackApi(Subject):

    _default_callback_message_type = 'incoming_message'
    _default_data = {'user': 'bdgwsh', 'msg': 'hello'}

    def __init__(self):
        self._observers = []
        self._message = {'message_type': self._default_callback_message_type, 'data': self._default_data}

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = {'message_type': value['message_type'],  'data': value['data']}

    def send_message(self):
        self.notify()


class MemeBotServer(Observer):

    def update(self, subject):
        vk_message = subject.message
        self.process_message(vk_message)

    def process_message(self, message):
        print(f'{self.__class__.__name__} processing message {message}')


class MovieBotServer(Observer):

    def update(self, subject):
        vk_message = subject.message
        self.process_message(vk_message)

    def process_message(self, message):
        print(f'{self.__class__.__name__} processing message {message}')


if __name__ == '__main__':
    mem_bot_server = MemeBotServer()
    movie_bot_server = MovieBotServer()

    vk_callback_service = VkCallbackApi()
    vk_callback_service.attach(mem_bot_server)
    vk_callback_service.attach(movie_bot_server)

    vk_callback_service.message = {'message_type': 'incoming_msg',  'data': {'user_id': 1, 'msg': 'hello!'}}
    vk_callback_service.send_message()
    print()

    vk_callback_service.message = {'message_type': 'incoming_msg',  'data': {'user_id': 2, 'msg': 'hello there!'}}
    vk_callback_service.send_message()
