import sqlite3

# Función para inicializar la base de datos
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        telegram_username TEXT,
        chat_id INTEGER,
        wallet TEXT,
        email TEXT,
        twitter TEXT,
        subscription_days INTEGER
    )
    ''')
    conn.commit()
    conn.close()

# Función para añadir un usuario
def add_user(telegram_username, chat_id, wallet, email, twitter, subscription_days):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    INSERT INTO users (telegram_username, chat_id, wallet, email, twitter, subscription_days)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (telegram_username, chat_id, wallet, email, twitter, subscription_days))
    conn.commit()
    conn.close()

# Función para actualizar los días de suscripción de un usuario
def update_subscription_days(chat_id, days):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    UPDATE users
    SET subscription_days = subscription_days + ?
    WHERE chat_id = ?
    ''', (days, chat_id))
    conn.commit()
    conn.close()

# Función para obtener un usuario por telegram_username
def get_user_by_username_find(telegram_username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM users WHERE telegram_username = ?
    ''', (telegram_username,))
    user = c.fetchone()
    conn.close()
    return user

#Función para obtener un usuario por telergam_username
def get_user_by_username(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM users WHERE telegram_username = ?
    ''', (username,))
    user = c.fetchone()
    conn.close()
    if user:
        user_dict = {
            'id': user[0],
            'telegram_username': user[1],
            'chat_id': user[2],
            'wallet': user[3],
            'email': user[4],
            'twitter': user[5],
            'subscription_days': user[6]
        }
        return user_dict
    else:
        return None

# Función para obtener un usuario por chat_id
def get_user_by_chat_id(chat_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM users WHERE chat_id = ?
    ''', (chat_id,))
    user = c.fetchone()
    conn.close()
    return user

# Función para obtener los usuarios por dias de suscripcion
def get_user_by_subscription_days(days):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM users WHERE subscription_days <= ?
    ''', (days,))
    users = c.fetchall()
    conn.close()
    return users

# Función para obtener todos los usuarios
def get_all_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM users
    ''')
    users = c.fetchall()
    conn.close()
    return users

# Función para eliminar usuarios con 0 días de suscripción
def delete_users_with_zero_days():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE subscription_days <= 0")
    deleted_count = c.rowcount  #Obtenemos el numero de usuarios eliminados
    conn.commit()
    conn.close()
    return deleted_count

# Función para actualizar el correo electrónico de un usuario
def update_user_email(chat_id, new_email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET email = ? WHERE chat_id = ?", (new_email, chat_id))
    conn.commit()
    conn.close()

# Función para actualizar el usuario de Twitter de un usuario
def update_user_twitter(chat_id, new_twitter):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET twitter = ? WHERE chat_id = ?", (new_twitter, chat_id))
    conn.commit()
    conn.close()

# Función para actualizar la billetera Ethereum de un usuario
def update_user_wallet(chat_id, new_wallet):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET wallet = ? WHERE chat_id = ?", (new_wallet, chat_id))
    conn.commit()
    conn.close()


# Función para verificar si la wallet está asociada a otro usuario
def is_wallet_associated_with_another_user(wallet, current_user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    SELECT id FROM users WHERE wallet = ? AND id != ?
    ''', (wallet, current_user_id))
    user = c.fetchone()
    conn.close()
    return user is not None

# Función para obtener el balance de suscripción de un usuario
def get_subscription_balance(chat_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    SELECT subscription_days FROM users WHERE chat_id = ?
    ''', (chat_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return user[0]
    else:
        return None
    
# Inicializar la base de datos al cargar el módulo
init_db()

#BrandonFilth|-4278497926|0x6d465F5CB6FFc918761d4cC9A675F1ED2c6bB764|brandonfilth1@gmail.com|BrandonFilth1|30