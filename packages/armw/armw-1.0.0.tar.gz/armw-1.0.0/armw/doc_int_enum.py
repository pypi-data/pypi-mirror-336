from enum import IntEnum


class DocIntEnum(IntEnum):
    def __new__(cls, value, doc=None):
        self = int.__new__(cls, value)  # calling super().__new__(value) here would fail
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        else:
            self.__doc__ = ''
        return self

    @property
    def info(self):
        return f'{self.__class__}:{self.name}:[{self.value}]: {self.__doc__}'

    @classmethod
    def _get_field_index(cls, key: int):
        try:
            member_list = list(cls.__members__.items())
            for i in range(len(member_list)):  # Have to search through, because we might not have sequential values
                member = member_list[i]
                value = int(member[1])
                if value == key:
                    return i
            return None
        except IndexError:
            return None

    @classmethod
    def get_field(cls, key: int):
        index = cls._get_field_index(key)

        if index is not None:
            return list(cls.__members__.items())[index][1]
        else:
            return None

    @classmethod
    def get_field_names(cls):
        fields = list(cls.__members__.items())
        return [str(field[0]) for field in fields]

    @classmethod
    def get_field_name(cls, key: int):
        index = cls._get_field_index(key)

        if index is not None:
            return list(cls.__members__.items())[index][0]
        else:
            return None

    @classmethod
    def get_description(cls, key: int):
        """
        Attempts to return the best description of a field that it can
        """

        doc = cls.get_field(key).__doc__
        if len(doc) > 0:
            return doc
        else:
            return cls.get_field_name(key)
