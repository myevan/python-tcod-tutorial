import inspect

class FieldType:
    __seq = 0

    @classmethod
    def alloc_sequence(cls):
        cls.__seq += 1
        return cls.__seq

    def __init__(self, type_default, count=None, pk=False, fk=None, default=None):
        self._seq = FieldType.alloc_sequence()
        self._count = count
        self._pk = pk
        self._fk = fk
        self._default_value = type_default if default is None else default
        self._name = None
        self._parent_cls = None

    def bind(self, parent_cls, name):
        self._parent_cls = parent_cls
        self._name = name

    def __repr__(self):
        return self._parent_cls.__name__ + '.' + self._name

    @property
    def name(self):
        return self._name

    @property
    def default_value(self):
        return self._default_value

    @property
    def foreign_key(self):
        return self._fk

    @property
    def is_primary_key(self):
        return self._pk


class Integer(FieldType):
    def __init__(self, *args, **kwargs):
        FieldType.__init__(self, 0, *args, **kwargs)
    
class String(FieldType):
    def __init__(self, *args, **kwargs):
        FieldType.__init__(self, "", *args, **kwargs)

class DeclMeta(type):
    def __new__(meta, cls_name, bases, cls_dict):
        new_cls = type.__new__(meta, cls_name, bases, cls_dict)

        field_pairs = inspect.getmembers(new_cls, lambda m:isinstance(m, FieldType))
        for field_name, field_type in field_pairs:
            field_type.bind(new_cls, field_name)

        if field_pairs:
            field_pairs.sort(key=lambda x: x[1]._seq)
            new_cls._field_names, new_cls._field_types = list(zip(*field_pairs))
        else:
            new_cls._field_names = []
            new_cls._field_types = []

        new_cls._pk_names = [field_type.name for field_type in new_cls._field_types if field_type.is_primary_key]

        return new_cls

class Base(metaclass=DeclMeta):
    __records = list()
    __pk_records = dict()
    __repr_limit = 3

    @classmethod
    def get_field_names(cls):
        return cls._field_names

    @classmethod
    def get_primary_key_names(cls):
        return cls._pk_names

    @classmethod
    def get_field_types(cls):
        return cls._field_types

    def __init__(self, *args, **kwargs):
        for name, value in zip(self._field_names, args):
            setattr(self, name, value)

        for field_type in self._field_types[len(args):]:
            setattr(self, field_type.name, kwargs.get(field_type.name, field_type.default_value))

    def __repr__(self):
        name = self.__class__.__name__
        info = ' '.join(f"{key}={value}" for key, value in self.gen_field_pairs(limit=self.__repr_limit))
        return f"<{name} {info}>"

    @classmethod
    def load_datas(cls, datas):
        cls.__records = [cls(*data) for data in datas]
        if cls._pk_names:
            cls.__pk_records = dict((record.get_primary_key_values(), record) for record in cls.__records)

    @classmethod
    def get(cls, pk):
        assert(cls.__pk_records)
        return cls.__pk_records[pk]

    def gen_field_pairs(self, limit=None):
        if limit is None:
            for name in self._field_names:
                yield (name, getattr(self, name))
        else:
            for name in self._field_names[:limit]:
                yield (name, getattr(self, name))

    def get_primary_key_values(self):
        assert(self._pk_names)
        if len(self._pk_names) == 1:
            return getattr(self, self._pk_names[0])
        else:
            return tuple(getattr(self, name) for name in self._pk_names)


if __name__ == '__main__':
    class User(Base):
        id = Integer(pk=True)
        name = String()

    class Profile(Base):
        id = Integer(pk=True)
        user_id = Integer(fk=User.id)

    print(list(User(name="haha").gen_field_pairs()))
    print(Profile.user_id.foreign_key)
