from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.CharField(max_length=100, verbose_name='Почта')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingMessage(models.Model):
    subject = models.CharField(max_length=200, **NULLABLE, verbose_name='Тема')
    message = models.TextField(verbose_name='Тело')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingSettings(models.Model):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    PERIODS = (
        (DAILY, 'Ежедневная'),
        (WEEKLY, 'Еженедельная'),
        (MONTHLY, 'Ежемесячная'),
    )

    CREATED = 'created'
    STARTED = 'started'
    DONE = 'done'

    STATUS = (
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
        (DONE, 'Завершена'),
    )

    start_time = models.DateTimeField(verbose_name='Время начала рассылки')
    end_time = models.DateTimeField(verbose_name='Время окончания рассылки')
    period = models.CharField(max_length=20, choices=PERIODS, default=DAILY, verbose_name='Период')
    status = models.CharField(max_length=20, choices=STATUS, default=CREATED, verbose_name='Статус')

    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)

    def __str__(self):
        return f'{self.start_time} - {self.end_time} / {self.period} / {self.status}'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class MailingClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройка')

    def __str__(self):
        return f'{self.client} / {self.settings}'

    class Meta:
        verbose_name = 'Клиент рассылки'
        verbose_name_plural = 'Клиенты рассылки'


class MailingLog(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'

    STATUS = (
        (STATUS_OK, 'Ok'),
        (STATUS_FAILED, 'Failed'),
    )

    last_try = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    status = models.CharField(choices=STATUS, default=STATUS_OK, verbose_name='Статус попытки')
    server_response = models.TextField(**NULLABLE, verbose_name='Ответ почтового сервера')

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройка')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
