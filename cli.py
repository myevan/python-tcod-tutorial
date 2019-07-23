import logging

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

if __name__ == '__main__':
    import click
    
    @click.group()
    def cli(): pass

    @cli.command()
    def prepare():
        download_file(
            remote_file_path='https://github.com/libtcod/python-tcod/raw/master/fonts/libtcod/arial10x10.png',
            local_file_path='fonts/font.png')

    logging.basicConfig(level=logging.DEBUG)
    cli()

