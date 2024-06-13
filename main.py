import telebot
import threading
from daily_update import schedule_daily_update, start_scheduler
from user_registration import register_user_handlers
from admin_commands import register_admin_handlers
from user_commands import register_user_commands 

# Crear el objeto bot con el token
bot = telebot.TeleBot("7103546649:AAG4XiXmRjIcXdd-6dmoWq4eYfFJpLFYB5U")

#              dev        kakarot
admin_ids = [1737264011, 1602791885]

group_id = "-1001852742291" 

# Iniciar el hilo para la actualización diaria de suscripciones
subscription_thread = threading.Thread(target=schedule_daily_update, args=(bot, admin_ids))
subscription_thread.daemon = True
subscription_thread.start()

# Iniciar el hilo para el scheduler
scheduler_thread = threading.Thread(target=start_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

# Registrar los handlers de usuario y administrador
register_user_handlers(bot, admin_ids, group_id)
register_admin_handlers(bot, admin_ids)
register_user_commands(bot)

# Iniciar el bot
bot.polling()
