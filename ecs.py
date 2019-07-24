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

class Entity:
    def __init__(self, id, comps):
        self.id = id
        self.comps = dict((comp.get_sequence(), comp) for comp in comps)

    def get_component_sequences(self):
        return self.comps.keys()

    def get_id(self):
        return self.id

class System:
    _inst = None

    @classmethod
    def get(cls):
        if not cls._inst:
            cls._inst = cls()
        return cls._inst

    def __init__(self):
        self.world = None

    def bind(self, world):
        self.world = world

    def start(self):
        return True

    def stop(self):
        return

    def update(self):
        pass

class World:
    def __init__(self):
        self.is_alive = True
        self.next_entity_id = 0
        self.entities = OrderedDict()
        self.components = defaultdict(dict)
        self.systems = []

    def create_entity(self, *comps):
        self.next_entity_id += 1

        new_entity_id = self.next_entity_id
        new_entity = Entity(new_entity_id, comps)
        self.entities[new_entity_id] = new_entity

        for comp in comps:
            comp_seq = comp.get_sequence()
            self.components[comp.get_sequence()][new_entity_id] = comp

        return new_entity

    def destroy_entity(self, del_entity_id):
        del_entity =  self.entities.get(del_entity_id)
        if del_entity:
            for comp_seq in del_entity.get_component_sequences():
                del self.components[comp_seq][del_entity_id] 
                
            del self.entities[del_entity_id]
        
    def get_entity_pairs(self):
        return self.entities.items()

    def get_entity_component(self, entity_id, comp_cls):
        comp_seq = comp_cls.get_sequence()
        return self.components[comp_seq][entity_id]

    def get_component_pairs(self, comp_cls):
        comp_seq = comp_cls.get_sequence()
        return self.components[comp_seq].items()

    def get_components(self, comp_cls):
        comp_seq = comp_cls.get_sequence()
        return self.components[comp_seq].values()

    def add_system(self, system):
        system.bind(self)
        self.systems.append(system)
        return system

    def start(self):
        for system in self.systems:
            if not system.start():
                return False

        return True

    def stop(self):
        for system in self.systems:
            system.stop()

    def update(self):
        if not self.is_alive:
            return False

        for system in self.systems:
            system.update()

        return True

    def kill(self):
        self.is_alive = False

        

