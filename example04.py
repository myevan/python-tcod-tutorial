import mdb
import ecs
import evs

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

class AppClosingEvent(evs.Event):
    pass

class PlayerMovingEvent(evs.Event):
    def __init__(self, dx, dy):
        self.dx = dx 
        self.dy = dy

class ControlSystem(ecs.System, evs.EventHandler):
    def start(self):
        event_system = evs.EventSystem.get()
        event_system.add_event_handler(PlayerMovingEvent, self)
        event_system.add_event_handler(AppClosingEvent, self)

    def set_player_eid(self, eid):
        self.player_eid = eid

    def recv_event(self, event):
        if PlayerMovingEvent.is_instance(event):
            comp = self.world.get_entity_component(self.player_eid, CharacterComponent)
            comp.x += event.dx
            comp.y += event.dy
        elif AppClosingEvent.is_instance(event):
            self.world.kill()
   
import tcod

class InputSystem(ecs.System):
    vk_events = {
        tcod.KEY_ESCAPE: AppClosingEvent(),
        tcod.KEY_UP: PlayerMovingEvent(0, -1),
        tcod.KEY_DOWN: PlayerMovingEvent(0, +1),
        tcod.KEY_LEFT: PlayerMovingEvent(-1, 0),
        tcod.KEY_RIGHT: PlayerMovingEvent(+1, 0),
    }

    def update(self):
        event_system = evs.EventSystem.get()
        if tcod.console_is_window_closed():
            event_system.send_event(AppClosingEvent())
            return

        key = tcod.console_check_for_keypress()
        event = self.vk_events.get(key.vk)
        if event:
            event_system.send_event(event)


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
    world.add_system(evs.EventSystem.get())
    world.add_system(InputSystem.get())
    world.add_system(ControlSystem.get())
    world.add_system(RenderSystem.get())
    world.start()

    entity = world.create_entity(CharacterComponent(1, 40, 30))
    ControlSystem.get().set_player_eid(entity.get_id())

    while world.update():
        pass

    world.destroy_entity(entity.get_id())
    world.stop()

