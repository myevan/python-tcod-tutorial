import tcod
tcod.console_set_custom_font('fonts/font.png', flags=tcod.FONT_TYPE_GREYSCALE|tcod.FONT_LAYOUT_TCOD)
tcod.console_init_root(w=80, h=60, title='example', fullscreen=False)
tcod.sys_set_fps(30)

x = 40
y = 30

while not tcod.console_is_window_closed():
    tcod.console_set_default_foreground(0, tcod.white)
    tcod.console_put_char(0, x, y, '@', tcod.BKGND_NONE)
    tcod.console_flush()
    tcod.console_put_char(0, x, y, ' ', tcod.BKGND_NONE)

    key = tcod.console_check_for_keypress()
    if key.vk == tcod.KEY_ESCAPE:
        break
    elif key.vk == tcod.KEY_UP:
        y -= 1
    elif key.vk == tcod.KEY_DOWN:
        y += 1
    elif key.vk == tcod.KEY_LEFT:
        x -= 1
    elif key.vk == tcod.KEY_RIGHT:
        x += 1

