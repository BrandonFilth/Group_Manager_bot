import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pay_verification import verify_eth_transaction
from group import generate_invite_link
from database import add_user, get_user_by_chat_id, update_subscription_days, update_user_email, update_user_twitter

destination_wallet = "0x2ec487661b101fd2cf32cbda392414bb9b2a5c5b"

def register_user_handlers(bot, admin_ids, group_id):

    @bot.message_handler(commands=['start'])
    def start(message):
        instructions = (
            f"*Buenas hijo del demonio 👹*\n\n"
            f"Para acceder al grupo hay que realizar un pago de 25 dólares a la wallet:\n\n"
            f"📑: `{destination_wallet}`\n\n"
            "El pago solamente se puede realizar con USDT o con ETH en la red Base ⏺\n\n"
            "Una vez hecho el pago, el Bot verificará la transacción y te dará acceso al grupo Kakarot Trading Club.\n\n"
            "Por cada 25 dólares recibirás 30 días de acceso al grupo y a todo el contenido.\n\n"
            "Por favor, antes de realizar el pago asegúrate y verifica que no haya ningún error.\n\n"
            "**Presiona el botón una vez hayas realizado el pago:**"
        )
        markup = InlineKeyboardMarkup()
        button_paid = InlineKeyboardButton("He pagado", callback_data='payment_confirmed')
        markup.add(button_paid)
        # Limpia cualquier teclado anterior
        telebot.types.ReplyKeyboardRemove()
        # Envía el mensaje con el botón
        bot.send_message(message.chat.id, instructions, reply_markup=markup, parse_mode='Markdown')

    # Manejar la acción al presionar el botón "He pagado"
    @bot.callback_query_handler(func=lambda call: call.data == 'payment_confirmed')
    def handle_payment_confirmation(call):
        bot.send_message(call.message.chat.id, "Por favor, ingresa tu dirección de billetera Ethereum:")
        bot.register_next_step_handler(call.message, process_eth_wallet_input)

    def process_eth_wallet_input(message):
        eth_user_wallet = message.text
        bot.send_message(message.chat.id, "Validando transacción...")

        try:
            # Verificar la transacción
            success, result = verify_eth_transaction(eth_user_wallet, destination_wallet, message.from_user.id)
        except Exception as e:
            
            bot.send_message(message.chat.id, f"Ocurrió un error al validar la transacción. Por favor, intenta nuevamente.")
            return

        if success:
            tx_hash = result
            tx_url = f"https://basescan.org/tx/{tx_hash}"
            bot.send_message(message.chat.id, f"Transacción validada. Puedes verificarla en el siguiente enlace: {tx_url}")
            print("pago")
            # Verificar si el usuario ya está en la base de datos
            user = get_user_by_chat_id(message.chat.id)
            if user:
                print("existe")
                update_subscription_days(message.chat.id, 30)
                new_balance = user[6] + 30
                bot.send_message(message.chat.id, "¡Pago confirmado! Tu suscripción ha sido extendida 30 días más.")
                
                # Notificar a los administradores
                for admin_id in admin_ids:
                    bot.send_message(admin_id, f"El usuario @{message.from_user.username} ha extendido su suscripción con la wallet {eth_user_wallet}.")
            else:
                # Llamar a la función con el bot y el ID del grupo de manera asíncrona
                invite_link = generate_invite_link(bot, group_id)

                if invite_link:
                    markup = InlineKeyboardMarkup()
                    button_invite = InlineKeyboardButton("Invitar al grupo", url=invite_link)
                    markup.add(button_invite)
                    bot.send_message(message.chat.id, "Haz clic en 'Invitar al grupo' para unirte al grupo privado:", reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, "Hubo un problema al generar el enlace de invitación. Por favor, contacta a un administrador.")
        
                # Solicitar el usuario de Twitter y email para usuarios nuevos
                bot.send_message(message.chat.id, "Por favor, ingresa tu usuario de Twitter:")
                bot.register_next_step_handler(message, process_twitter_input, eth_user_wallet)
        else:
            error_message = result
            bot.send_message(message.chat.id, f"No se encontró una transacción válida. {error_message} Por favor, asegúrate de haber pagado correctamente.")

    def process_twitter_input(message, eth_user_wallet):
        twitter = message.text
        bot.send_message(message.chat.id, "Por favor, ingresa tu correo electrónico:")
        bot.register_next_step_handler(message, process_email_input, eth_user_wallet, twitter)

    # Registro de cuenta de email
    def process_email_input(message, eth_user_wallet, twitter):
        email = message.text
        telegram_username = message.from_user.username
        chat_id = message.chat.id
        
        # Agregar el usuario nuevo a la base de datos
        add_user(telegram_username, chat_id, eth_user_wallet, email, twitter, 30)

        # Mostrar datos al usuario con botones para editar o confirmar
        confirmation_text = f"Por favor, confirma tus datos:\nTwitter: {twitter}\nEmail: {email}\nWallet: {eth_user_wallet}"
        markup = InlineKeyboardMarkup()
        button_edit = InlineKeyboardButton("Editar", callback_data='edit_data')
        button_confirm = InlineKeyboardButton("Confirmar", callback_data='confirm_data')
        markup.add(button_edit, button_confirm)
        bot.send_message(chat_id, confirmation_text, reply_markup=markup)

        # Notificar a los administradores
        for admin_id in admin_ids:
            bot.send_message(admin_id, f"El usuario: @{telegram_username} se ha suscrito con la wallet {eth_user_wallet}.")

        # Manejar la confirmación o edición de datos
        @bot.callback_query_handler(func=lambda call: call.data in ['edit_data', 'confirm_data'])
        def handle_data_confirmation(call):
            if call.data == 'confirm_data':
                bot.send_message(call.message.chat.id, "Tus datos han sido confirmados. ¡Gracias!")
            elif call.data == 'edit_data':
                edit_text = "Selecciona una opción a editar:"
                markup = InlineKeyboardMarkup()
                button_twitter = InlineKeyboardButton("Twitter", callback_data='edit_twitter')
                button_email = InlineKeyboardButton("Email", callback_data='edit_email')
                markup.add(button_twitter, button_email)
                bot.edit_message_text(edit_text, call.message.chat.id, call.message.message_id, reply_markup=markup)

        # Manejar la edición de Twitter o Email
        @bot.callback_query_handler(func=lambda call: call.data in ['edit_twitter', 'edit_email'])
        def handle_edit_selection(call):
            if call.data == 'edit_twitter':
                bot.send_message(call.message.chat.id, "Por favor, ingresa tu nuevo usuario de Twitter:")
                bot.register_next_step_handler(call.message, update_twitter, eth_user_wallet, email)
            elif call.data == 'edit_email':
                bot.send_message(call.message.chat.id, "Por favor, ingresa tu nuevo correo electrónico:")
                bot.register_next_step_handler(call.message, update_email, eth_user_wallet, twitter)

    def update_email(message, eth_user_wallet, twitter):
        new_email = message.text
        update_user_email(message.chat.id, new_email)
        show_updated_info(message.chat.id, twitter, new_email, eth_user_wallet, message.from_user.username)

    def update_twitter(message, eth_user_wallet, email):
        new_twitter = message.text
        update_user_twitter(message.chat.id, new_twitter)
        show_updated_info(message.chat.id, new_twitter, email, eth_user_wallet, message.from_user.username)

    def show_updated_info(chat_id, twitter, email, eth_user_wallet, telegram_username):
        updated_info = f"Tus datos han sido actualizados:\nTwitter: {twitter}\nEmail: {email}\nWallet: {eth_user_wallet}"
        bot.send_message(chat_id, updated_info)

