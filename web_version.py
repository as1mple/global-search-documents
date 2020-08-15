import eel

from search import get_doc


@eel.expose
def wrapper(search, count):
    return get_doc(search, count)


eel.init('web')
eel.start('main.html', size=(2000, 1000))
