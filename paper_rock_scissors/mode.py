from abc import ABCMeta, abstractmethod

from _role import Player, Computer


class BaseMode(metaclass=ABCMeta):

    @abstractmethod
    def __init__(
            self, first_role, first_name, first_score,
            second_role, second_name, second_score, **kwargs):
        self.first_role = first_role
        self.first_name = first_name
        self.first_score = first_score
        self.second_role = second_role
        self.second_name = second_name
        self.second_score = second_score

        for key in kwargs:
            setattr(self, key, kwargs[key])

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def make_first_player(self):
        pass

    @abstractmethod
    def make_second_player(self):
        pass


class StandardMode(BaseMode):

    def __init__(
            self, first_role, first_name, first_score,
            second_role, second_name, second_score, **kwargs):
        super().__init__(
            first_role, first_name, first_score,
            second_role, second_name, second_score, **kwargs)

    def __str__(self):
        return '\n\n\t------ Standard Mode ------'

    def make_first_player(self):
        return Player(
            self.first_role,
            self.first_name,
            self.first_score
        )

    def make_second_player(self):
        return Computer(
            self.second_role,
            self.second_name,
            self.second_score,
            getattr(self, 'seed')
        )


class DualMode(BaseMode):

    def __init__(
            self, first_role, first_name, first_score,
            second_role, second_name, second_score, **kwargs):
        super().__init__(
            first_role, first_name, first_score,
            second_role, second_name, second_score, **kwargs)

    def __str__(self):
        return '\n\n\t------ Dual Mode ------'

    def make_first_player(self):
        return Player(
            self.first_role,
            self.first_name,
            self.first_score
        )

    def make_second_player(self):
        return Player(
            self.second_role,
            self.second_name,
            self.second_score
        )


class AIMode(BaseMode):

    def __init__(
            self, first_role, first_name, first_score,
            second_role, second_name, second_score, **kwargs):
        super().__init__(
            first_role, first_name, first_score,
            second_role, second_name, second_score, **kwargs)

    def __str__(self):
        return '\n\n\t------ AI Mode ------'

    def make_first_player(self):
        return Computer(
            self.first_role,
            self.first_name,
            self.first_score,
            getattr(self, 'seed')
        )

    def make_second_player(self):
        return Computer(
            self.second_role,
            self.second_name,
            self.second_score,
            getattr(self, 'seed')
        )
