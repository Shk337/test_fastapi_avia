#request_body = {
#     "message": "asdfa",
#     "time": "2022-10-17:22-18",
#     "email": "nomercy13.37@yandex.ru"
# }
# Request body должен обработаться используя Fast Api

# Задание:
# Я должен в Постмане отправить запрос и указать время отправки  моего сообщения
# и Адресат Кому. Мини Запланированная отправка емэйла

from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

from settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class EmailSchema(BaseModel):
    message: str
    time: datetime | str | None = datetime.now() + timedelta(seconds=10)
    email: EmailStr


conf = ConnectionConfig(MAIL_USERNAME="shoockerz",
                        MAIL_PASSWORD=settings.EMAIL_PASSWORD,
                        MAIL_FROM=settings.EMAIL_LOGIN,
                        MAIL_PORT=587,
                        MAIL_SERVER="smtp.gmail.com",
                        MAIL_FROM_NAME="FastAPI",
                        MAIL_STARTTLS=True,
                        MAIL_SSL_TLS=False,
                        USE_CREDENTIALS=True,
                        VALIDATE_CERTS=True)

app = FastAPI()


@app.post("/email", description="отправка сообщений на почту")
async def route(item: EmailSchema) -> JSONResponse | dict[str, str]:
    try:
        await add_task(item.email, item.message, item.time)
    except Exception as ex:
        return JSONResponse(status_code=400, content={"message": str(ex)})
    return {
        "info": "email has been sent ",
        "message": str(item.message),
        "time": str(item.time),
        "email": str(item.email)
    }


async def add_task(email: str, message: str, time_message: str) -> None:
    logger.debug(f'curent time = {datetime.now()}')
    scheduler = AsyncIOScheduler()

    try:
        scheduler.add_job(simple_send,
                          'date',
                          run_date=datetime.strptime(time_message,
                                                     "%Y-%m-%d:%H-%M"),
                          args=[message, email])
        scheduler.start()
    except:
        scheduler.add_job(simple_send,
                          'date',
                          run_date=time_message,
                          args=[message, email])
        scheduler.start()


async def simple_send(message, email) -> None:
    html = """message: {}""".format(message)

    message = MessageSchema(subject="Заголовок",
                            recipients=[email],
                            body=html,
                            subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    logger.info("email has been sent")