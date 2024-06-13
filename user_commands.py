import telebot
from database import get_subscription_balance

def register_user_commands(bot):
    @bot.message_handler(commands=['subscription_balance'])
    def handle_subscription_balance(message):
        chat_id = message.chat.id
        days = get_subscription_balance(chat_id)
        if days is not None:
            response = f"Tienes {days} días de suscripción restantes."
        else:
            response = "No cuentas con una suscripción activa."
        bot.reply_to(message, response)
