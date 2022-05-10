from django.db import models
from django.utils.safestring import mark_safe
class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(TimeBasedModel):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
    user_id = models.BigIntegerField(unique=True, default=1, verbose_name="ID Пользователя Телеграм")
    name = models.CharField(max_length=100,  verbose_name="Имя Пользователя")
    username = models.CharField(unique=True, max_length=100,  verbose_name="Username Телеграм")

    def __str__(self):
        return f"{self.name} - {self.username}"


class Request(TimeBasedModel):
    class Meta:
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"
    
    TYPE_REQUEST = (
        ('3D', '3д печать'),
        ('laser', 'Лазерная резка')
    )

    READINESS = (
        (1, '?'),
        (2, 'принят'),
        (3, 'в работе'),
        (4, 'готов'),
        (5, 'вручен'),
    )

    name_user = models.ForeignKey(User, verbose_name="Заказчик", on_delete=models.SET(0))
    name_product = models.CharField(verbose_name="Имя заказа", max_length=100)
    type_request = models.CharField(verbose_name="Тип Запроса", choices=TYPE_REQUEST, max_length=100)
    quantity = models.IntegerField(verbose_name="Количество")
    promptness = models.IntegerField(verbose_name="Степень срочности", )
    comment = models.CharField(verbose_name="Комментарий", max_length=5000, null=True)
    readiness = models.IntegerField(verbose_name="Готовность", choices=READINESS, default=1)
    path_to_file = models.CharField(unique=True, verbose_name="Путь до файла", max_length=1000, null=True)

    def __str__(self):
        return f"№{self.id} - {self.name_product}({self.quantity})"
    
    def fieldname_download(self):
        return mark_safe('<a href="/{0}" download>Скачать</a>'.format(
            self.path_to_file, self.path_to_file))

    fieldname_download.short_description = 'Скачать Файл'
