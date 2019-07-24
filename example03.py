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

class ControlSystem(ecs.System):
    def __init__(self, entity_id):
        ecs.System.__init__(self)
        self.player_eid = entity_id

    def update(self):
        if tcod.console_is_window_closed():
            self.world.kill()
            return

        key = tcod.console_check_for_keypress()
        if key.vk == tcod.KEY_ESCAPE:
            self.world.kill()
            return

        comp = world.get_entity_component(self.player_eid, CharacterComponent)
        if key.vk == tcod.KEY_UP:
            comp.y -= 1
        elif key.vk == tcod.KEY_DOWN:
            comp.y += 1
        elif key.vk == tcod.KEY_LEFT:
            comp.x -= 1
        elif key.vk == tcod.KEY_RIGHT:
            comp.x += 1


class RenderSystem(ecs.System):
    def __init__(self, *args, **kwargs):
        ecs.System.__init__(self, *args, **kwargs)

        tcod.console_set_custom_font('fonts/font.png', flags=tcod.FONT_TYPE_GREYSCALE|tcod.FONT_LAYOUT_TCOD)
        tcod.console_init_root(w=80, h=60, title='example', fullscreen=False)
        tcod.sys_set_fps(30)

    def update(self):
        for comp in self.world.get_components(CharacterComponent):
            tcod.console_set_default_foreground(0, tcod.white)
            tcod.console_put_char(0, comp.x, comp.y, comp.char_proto.shape, tcod.BKGND_NONE)

        tcod.console_flush()

        for comp in self.world.get_components(CharacterComponent):
            tcod.console_set_default_foreground(0, tcod.white)
            tcod.console_put_char(0, comp.x, comp.y, ' ', tcod.BKGND_NONE)


if __name__ == '__main__':
    CharacterProto.load_datas([
        (1, '@'),
        (2, 'm'),
    ])

    world = ecs.World()
    entity = world.create_entity(CharacterComponent(1, 40, 30))
    world.add_system(ControlSystem(entity.get_id()))
    world.add_system(RenderSystem())
    world.start()

    while world.update():
        pass

    world.destroy_entity(entity.get_id())
    world.stop()

