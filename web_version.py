from search import get_doc

import eel
from loguru import logger

logger.add('debug.log', format="{time} {level} {message}", level="DEBUG", rotation="1 weeks", compression='zip')


@eel.expose
def wrapper(search, count):
    logger.info('Start searching')
    return get_doc(search, count)


@eel.expose
def save_proxy(new_proxy: str, path: str = 'setting.txt') -> bool:
    if status := (
            (new_proxy := new_proxy.replace('	', '').replace(' ', '')).replace('.', '').replace(':', '').isdigit()):
        logger.info(f'Proxy Editing => {new_proxy=}')
        with open(path, 'r+') as outfile:
            file = outfile.readlines()
            outfile.seek(0)
            file[2] = f'proxy={new_proxy}'
            outfile.writelines(file)
            outfile.truncate()
    else:
        logger.error('Invalid proxy format')
    return status


eel.init('web')
eel.start('main.html', size=(2000, 1000))
