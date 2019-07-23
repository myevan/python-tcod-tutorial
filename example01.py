import tcod
tcod.console_set_custom_font('fonts/font.png', flags=tcod.FONT_TYPE_GREYSCALE|tcod.FONT_LAYOUT_TCOD)
tcod.console_init_root(w=80, h=60, title='example', fullscreen=False)
tcod.sys_set_fps(30)

while not tcod.console_is_window_closed():
    tcod.console_set_default_foreground(0, tcod.white)
    tcod.console_put_char(0, 40, 30, '@', tcod.BKGND_NONE)
    tcod.console_flush()

    key = tcod.console_check_for_keypress()
    if key.vk == tcod.KEY_ESCAPE:
        break

