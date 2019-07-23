import mdb
import ecs

class CharacterProto(mdb.Base):
    pid = mdb.Integer(pk=True)
    shape = mdb.String()

class CharacterComponent(ecs.Component):
    char_pid = mdb.Integer()
    x = mdb.Integer()
    y = mdb.Integer()

    def __init__(self, *args, **kwargs):
        ecs.Component.__init__(self, *args, **kwargs)
        self.char_proto = CharacterProto.get(self.char_pid)

import tcod

class RenderingSystem(ecs.System):
    def __init__(self, entity_id, *args, **kwargs):
        ecs.System.__init__(self, *args, **kwargs)

        tcod.console_set_custom_font('fonts/font.png', flags=tcod.FONT_TYPE_GREYSCALE|tcod.FONT_LAYOUT_TCOD)
        tcod.console_init_root(w=80, h=60, title='example', fullscreen=False)
        tcod.sys_set_fps(30)

        self.entity_id = entity_id

    def pump(self, world):
        if tcod.console_is_window_closed():
            return False

        key = tcod.console_check_for_keypress()
        if key.vk == tcod.KEY_ESCAPE:
            return False

        comp = world.get_component(self.entity_id, CharacterComponent)
        if key.vk == tcod.KEY_UP:
            comp.y -= 1
        elif key.vk == tcod.KEY_DOWN:
            comp.y += 1
        elif key.vk == tcod.KEY_LEFT:
            comp.x -= 1
        elif key.vk == tcod.KEY_RIGHT:
            comp.x += 1

        return True

    def update(self, world):
        for comp in world.get_components(CharacterComponent):
            tcod.console_set_default_foreground(0, tcod.white)
            tcod.console_put_char(0, comp.x, comp.y, comp.char_proto.shape, tcod.BKGND_NONE)

        tcod.console_flush()

        for comp in world.get_components(CharacterComponent):
            tcod.console_set_default_foreground(0, tcod.white)
            tcod.console_put_char(0, comp.x, comp.y, ' ', tcod.BKGND_NONE)


if __name__ == '__main__':
    CharacterProto.load_datas([
        (1, '@'),
        (2, 'm'),
    ])

    world = ecs.World()
    new_entity = world.create_entity()
    world.add_component(new_entity.id, CharacterComponent(1, 40, 30))
    world.add_system(RenderingSystem(new_entity.id))

    while world.pump():
        world.update()


