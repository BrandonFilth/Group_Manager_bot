import telebot
from database import get_user_by_username, update_subscription_days, get_user_by_subscription_days, get_user_by_username_find, delete_users_with_zero_days
def register_admin_handlers(bot, admin_ids):

    # Comando para obtener la información de un usuario por su nombre de usuario de Telegram
    @bot.message_handler(commands=['get_user_info'])
    def get_user_info(message):
        # Verificar que el usuario sea un administrador
        if message.from_user.id not in admin_ids:
            bot.reply_to(message, "Este comando solo puede ser utilizado por los administradores.")
            return
        
        # Solicitar al administrador el nombre de usuario del usuario a consultar
        bot.send_message(message.chat.id, "Por favor, ingresa el nombre de usuario del usuario que deseas consultar:")
        bot.register_next_step_handler(message, process_username_input_for_info)

    def process_username_input_for_info(message):
        # Obtener el nombre de usuario del usuario a consultar
        username_to_find = message.text
        
        # Buscar al usuario en la base de datos
        user = get_user_by_username_find(username_to_find)
        if user:
            # Enviar la información del usuario al administrador
            chat_id, telegram_username, wallet, email, twitter, subscription_days = user[2], user[1], user[3], user[4], user[5], user[6]
            user_info = f"Nombre de usuario: {telegram_username}\nID de Chat: {chat_id}\nWallet: {wallet}\nCorreo Electrónico: {email}\nTwitter: {twitter}\nDías de suscripción restantes: {subscription_days}"
            bot.send_message(message.chat.id, user_info)
        else:
            bot.send_message(message.chat.id, f"No se encontró al usuario con nombre de usuario: {username_to_find}")

    # Comando para añadir días a un usuario (solo para administradores)
    @bot.message_handler(commands=['add_days'])
    def add_days_command(message):
        # Verificar si el usuario que envía el mensaje es un administrador
        if message.from_user.id not in admin_ids:
            bot.send_message(message.chat.id, "Este comando solo puede ser usado por administradores.")
            return

        # Solicitar al administrador el nombre de usuario
        bot.send_message(message.chat.id, "Por favor, ingresa el nombre de usuario:")
        bot.register_next_step_handler(message, process_username_input_for_add_days)

    def process_username_input_for_add_days(message):
        # Obtener el nombre de usuario ingresado por el administrador
        username = message.text.strip()

        # Solicitar al administrador la cantidad de días a añadir
        bot.send_message(message.chat.id, "Por favor, ingresa la cantidad de días a añadir:")
        bot.register_next_step_handler(message, process_days_input_for_add_days, username)

    def process_days_input_for_add_days(message, username):
        # Obtener la cantidad de días ingresada por el administrador
        try:
            days = int(message.text.strip())
        except ValueError:
            bot.send_message(message.chat.id, "Cantidad de días inválida. Debe ser un número entero.")
            return

        # Obtener el usuario por su nombre de usuario
        user = get_user_by_username(username)
        if not user:
            bot.send_message(message.chat.id, f"No se encontró al usuario {username}.")
            return

        # Añadir días a la suscripción del usuario
        update_subscription_days(user['chat_id'], days)
        bot.send_message(message.chat.id, f"Se han añadido {days} días al usuario {username}.")

    # Comando para mostrar usuarios con 0 días de balance
    @bot.message_handler(commands=['show_zero_balance_users'])
    def show_zero_balance(message):
        # Verificar que el usuario sea un administrador
        if message.from_user.id not in admin_ids:
            bot.reply_to(message, "Este comando solo puede ser utilizado por los administradores.")
            return
        
        # Modificar aquí para incluir usuarios con 0 o menos días de balance
        users_zero_balance = get_user_by_subscription_days(0) 
        
        if users_zero_balance:
            user_list = "\n".join([f"@{user[1]}" for user in users_zero_balance])
            response = f"Usuarios con 0 días de balance o menos:\n{user_list}"
        else:
            response = "No hay usuarios con 0 días de balance o menos."
        
        bot.send_message(message.chat.id, response)


    #comando para eliminar usuarios sin suscripción
    @bot.message_handler(commands=['delete_unsubscribed_users'])
    def delete_unsubscribed_users(message):
        # Verificar que el usuario sea un administrador
        if message.from_user.id not in admin_ids:
            bot.reply_to(message, "Este comando solo puede ser utilizado por los administradores.")
            return

        # Eliminar los usuarios con 0 días de suscripción de la base de datos
        deleted_count = delete_users_with_zero_days()
        
        # Enviar mensaje de confirmación o de no usuarios para eliminar
        if deleted_count > 0:
            bot.reply_to(message, "Todos los usuarios sin suscripción han sido eliminados de la base de datos.")
        else:
            bot.reply_to(message, "No hay usuarios para eliminar.")
