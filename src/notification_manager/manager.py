from requests import post
from config import TELEGRAM_TOKEN
from storage.users_schema import User
from storage import db_session
from apscheduler.schedulers.background import BlockingScheduler
from .content_functions import generate_notification_text


def send_notifications_to_all_users():
    """Отправляем уведомление каждому юзеру в БД"""

    for user in db_session.query(User).all():
        # Генерируем текст уведомления
        notification_text = generate_notification_text(user.user_id)

        # Заполняем строку запроса
        send_message_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?"
        send_message_url += f"chat_id={user.chat_id}&text={notification_text}&parse_mode=markdown"

        # Отправляем запрос
        post(send_message_url)


def create_manager():
    """Создание менеджера отложенных задач для регулярной отправки уведомлений"""

    scheduler = BlockingScheduler()
    scheduler.add_job(send_notifications_to_all_users, 'interval', minutes=2)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
