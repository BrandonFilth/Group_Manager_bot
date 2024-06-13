from telegram import Bot

def generate_invite_link(bot, group_id):
    try:
        # Generar un enlace de invitación de un solo uso
        invite_link = bot.create_chat_invite_link(chat_id=group_id, member_limit=1)
        print(invite_link.invite_link)
        return invite_link.invite_link  # Retorna solo el enlace
    except Exception as e:
        print(f"Error al generar el enlace de invitación: {e}")
        return None


