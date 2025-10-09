from log_settings import logger

def log_delete_user(username, user_id):
    logger.info(f'❌ Пользователь {username}, с id {user_id} удалён')

def log_register_user(username, user_id):
    logger.info(f'Пользователь {username}, с id {user_id} зарегестрирован')

def log_user_phone(username, user_id, phone):
    logger.info(f'Пользователь {username} с id {user_id} предоставил номер телефона: {phone}')