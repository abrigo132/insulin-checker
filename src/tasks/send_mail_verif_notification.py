from mailing import send_email
from core.models import User
from core import broker
from crud import UsersCrud
from core.models import db_helper


@broker.task
async def send_verification_message(user_id: int, verification_token: str) -> None:
    async with db_helper.session_factory() as session:
        user: User = await UsersCrud.get_user_by_id(
            session=session,
            user_id=user_id,
        )
    await send_email(
        recipient=user.email,
        subject="Thanks for register",
        body=f"Дорогой(-ая) {user.username}, \n\nСпасибо за регистрацию в нашем приложении"
        f" \n\nДля подтверждения регистрации пройдите по ссылке http://127.0.0.1:8080/api/v1/users/verification?verif_token={verification_token} \n\nНадеемся, что наше приложение вам понравится",
    )
    print("Сообщение отправлено пользователю!")
