import datetime
from smtplib import SMTPException

from django.core.mail import send_mail
from django.conf import settings
from mailing.models import MailingLog, MailingSettings


def send_email(mailing_settings, mailing_client):
    """Функция для отправки сообщения и создания лога"""

    status = ''
    server_response = ''

    try:
        result = send_mail(
            subject=mailing_settings.message.subject,
            message=mailing_settings.message.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[mailing_client.email],
            fail_silently=False
        )

        if result:
            status = MailingLog.STATUS_OK
            server_response = 'Отправка прошла успешно'

    except SMTPException as error:
        status = MailingLog.STATUS_FAILED
        server_response = str(error)

    MailingLog.objects.create(
        status=status,
        settings=mailing_settings,
        client_id=mailing_client.pk,
        server_response=server_response
    )


def send_mails():
    """Функция фильтрации рассылок, с последующей сменой статуса и отправкой сообщения клиенту"""
    datetime_now = datetime.datetime.now(datetime.timezone.utc)

    # получаем список всех созданных и запущенных рассылок
    for mailing_settings in MailingSettings.objects.exclude(status=MailingSettings.DONE):

        # проверяем дату окончания у рассылки для выставления статуса "Завершена"
        if datetime_now > mailing_settings.end_time:
            mailing_settings.status = MailingSettings.DONE

        # проверяем дату начала рассылки для выставления статуса "Запущена"
        elif datetime_now >= mailing_settings.start_time:
            mailing_settings.status = MailingSettings.STARTED

            # проходимся по каждому клиенту рассылки
            for mailing_client in mailing_settings.clients.all():

                # получаем лог текущего пользователя и текущей рассылки
                mailing_log = MailingLog.objects.filter(
                    client=mailing_client,
                    settings=mailing_settings
                )

                # если существуют логи с текущими клиентом и рассылкой
                # забираем последний лог и проверяем время для отправки
                if mailing_log.exists():
                    last_try_date = mailing_log.order_by('-last_try').first().last_try

                    if mailing_settings.period == MailingSettings.DAILY:
                        if (datetime_now - last_try_date).days >= 1:
                            send_email(mailing_settings, mailing_client)

                    elif mailing_settings.period == MailingSettings.WEEKLY:
                        if (datetime_now - last_try_date).days >= 7:
                            send_email(mailing_settings, mailing_client)

                    elif mailing_settings.period == MailingSettings.MONTHLY:
                        if (datetime_now - last_try_date).days >= 30:
                            send_email(mailing_settings, mailing_client)
                else:
                    send_email(mailing_settings, mailing_client)

        mailing_settings.save()
