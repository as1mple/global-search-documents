import eel

from search import get_doc


@eel.expose
def wrapper(search, count):
    return get_doc(search, count)


@eel.expose
def save_proxy(new_proxy: str, path: str = 'setting.txt') -> None:
    with open(path, 'r') as outfile:
        file = outfile.readlines()
        file[2] = f'proxy={new_proxy}'

    with open(path, 'w') as outfile:
        outfile.writelines(file)


eel.init('web')
eel.start('main.html', size=(2000, 1000))
