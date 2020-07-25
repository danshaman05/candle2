from flask import Blueprint

from .. import temporary_path   # TODO presunut do config filu

main = Blueprint('main', __name__)

@main .route(temporary_path + '/')
def home(): # TODO
    return f'<a href="{temporary_path}/miestnosti">Rozvrhy všetkých miestností</a>' \
           f'<br><a href="{temporary_path}/ucitelia">Rozvrhy všetkých učiteľov</a>' \
           f'<br><a href="{temporary_path}/kruzky">Rozvrhy všetkých krúžkov</a>'




