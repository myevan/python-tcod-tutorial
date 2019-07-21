import logging
logging.basicConfig(level=logging.DEBUG)

import os
import urllib.request

def download_file(local_file_path, remote_file_path):
    if os.path.isfile(local_file_path):
        logging.debug(f"found_local_file:{local_file_path}")
    else:
        logging.debug(f"download_remote_file:{remote_file_path}")
        file_data = urllib.request.urlopen(remote_file_path).read()

        local_dir_path = os.path.dirname(local_file_path)
        if not os.path.isdir(local_file_path):
            logging.debug(f"make_local_dir:{local_dir_path}")
            os.makedirs(local_dir_path)

        logging.debug(f"save_local_file:{local_file_path}")
        open(local_file_path, 'wb').write(file_data)

download_file(
    remote_file_path='https://github.com/libtcod/python-tcod/raw/master/fonts/libtcod/arial10x10.png',
    local_file_path='__fonts/font.png')

import tcod
tcod.console_set_custom_font('__fonts/font.png', flags=tcod.FONT_TYPE_GREYSCALE|tcod.FONT_LAYOUT_TCOD)
tcod.console_init_root(w=80, h=60, title='example', fullscreen=False)
tcod.sys_set_fps(30)

while not tcod.console_is_window_closed():
    tcod.console_set_default_foreground(0, tcod.white)
    tcod.console_put_char(0, 40, 30, '@', tcod.BKGND_NONE)
    tcod.console_flush()

    key = tcod.console_check_for_keypress()
    if key.vk == tcod.KEY_ESCAPE:
        break

