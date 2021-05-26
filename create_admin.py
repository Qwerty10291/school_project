from werkzeug.security import generate_password_hash
from db_additions import register_admin
from data.db_session import global_init

LOGIN = 'admin'
PASSWORD = 'nimda'
MAIL = 'admin@admin.ru'

global_init()
register_admin(LOGIN, generate_password_hash(PASSWORD), MAIL, 'admin')