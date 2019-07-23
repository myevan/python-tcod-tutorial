import mdb

from weakref import ref

from collections import OrderedDict
from collections import defaultdict

class SeqMeta(mdb.DeclMeta):
    __seq = 0

    @classmethod
    def alloc_sequence(meta):
        meta.__seq += 1
        return meta.__seq

    def __new__(meta, cls_name, bases, cls_dict):
        new_cls = mdb.DeclMeta.__new__(meta, cls_name, bases, cls_dict)
        new_cls._seq = meta.alloc_sequence()
        return new_cls

class Entity:
    def __init__(self, world_ref, id):
        self.world_ref = world_ref
        self.id = id

    def get_world(self):
        return self.world_ref()

class Component(metaclass=SeqMeta):
    @classmethod
    def get_sequence(cls):
        return cls._seq

    def __init__(self, *args, **kwargs):
        for name, value in zip(self._field_names, args):
            setattr(self, name, value)

        for field_type in self._field_types[len(args):]:
            setattr(self, field_type.name, kwargs.get(field_type.name, field_type.default_value))

    def __repr__(self):
        name = self.__class__.__name__
        info = ' '.join(f"{key}={value}" for key, value in self.gen_field_pairs(limit=self.__repr_limit))
        return f"<{name} {info}>"

class Storage:
    def __init__(self):
        self.entities = OrderedDict()
        self.comp_table = defaultdict(dict)

    def add_entity(self, entity):
        self.entities[entity.id] = entity
        return entity

    def get_entity(self, entity_id):
        return self.entities[entity_id]

    def get_entities(self):
        return self.entities.values()

    def add_component(self, entity_id, comp_seq, comp):
        self.comp_table[comp_seq][entity_id] = comp
        return comp

    def get_component(self, entity_id, comp_seq):
        return self.comp_table[comp_seq][entity_id]

    def get_components(self, comp_seq):
        return self.comp_table[comp_seq].values()

    def get_component_pairs(self, comp_seq):
        return self.comp_table[comp_seq].items()

class System:
    def pump(self, storage):
        return True

    def update(self, storage):
        pass

class World:
    def __init__(self):
        self.state = 1
        self.entity_id = 0
        self.storage = Storage()
        self.systems = []

    def create_entity(self):
        self.entity_id += 1
        return self.storage.add_entity(Entity(ref(self), self.entity_id))

    def add_system(self, system):
        self.systems.append(system)
        return system

    def add_component(self, entity_id, comp):
        comp_seq = comp.get_sequence()
        return self.storage.add_component(entity_id, comp_seq, comp)

    def get_component(self, entity_id, comp_cls):
        comp_seq = comp_cls.get_sequence()
        return self.storage.get_component(entity_id, comp_seq)

    def get_components(self, comp_cls):
        comp_seq = comp_cls.get_sequence()
        return self.storage.get_components(comp_seq)

    def get_component_pairs(self, comp_cls):
        comp_seq = comp_cls.get_sequence()
        return self.storage.get_component_pairs(comp_seq)

    def get_entities(self):
        return self.entities

    def pump(self):
        for system in self.systems:
            if not system.pump(self):
                return False

        return True

    def update(self):
        for system in self.systems:
            system.update(self)

