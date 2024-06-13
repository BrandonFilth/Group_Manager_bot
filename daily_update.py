import time
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
from database import get_all_users, update_subscription_days

def daily_subscription_update(bot, admin_ids):
    print("Actualizando suscripciones...")
    users = get_all_users()
    for user in users:
        chat_id, telegram_username, subscription_days = user[2], user[1], user[6]
        # Reducir los días de suscripción
        update_subscription_days(chat_id, -1)
        subscription_days -= 1  # Actualizar localmente después de la reducción

        # Enviar recordatorio si queda 1 día
        if subscription_days == 1:
            message = "Tu suscripción expira en 1 día. Por favor, renueva tu suscripción para seguir disfrutando del servicio."
            try:
                bot.send_message(chat_id, message)
            except Exception as e:
                print(f"No se pudo enviar el mensaje al chat con ID {chat_id}: {e}")

        # Notificar a los administradores si la suscripción ha expirado
        elif subscription_days == 0:
            message = f"El usuario {telegram_username} ({chat_id}) tiene 0 días de suscripción y debe ser eliminado."
            for admin_id in admin_ids:
                try:
                    bot.send_message(admin_id, message)
                except Exception as e:
                    print(f"No se pudo enviar el mensaje al chat con ID {admin_id}: {e}")

# Configurar el programador diario
scheduler = BlockingScheduler()

def schedule_daily_update(bot, admin_ids):
    # Programar la ejecución cada minuto
    scheduler.add_job(daily_subscription_update, 'interval', minutes=5, args=[bot, admin_ids])

# Iniciar el programador
def start_scheduler():
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
