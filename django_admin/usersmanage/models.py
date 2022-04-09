from django.db import models

class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(TimeBasedModel):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователь"
    
    id = models.AutoField(primary_kay=True)
    user_id = models.BigIntegerField(unique=True, default=1, verbose_name="ID Пользователя Телеграм")
    name = models.CharField(max_length=100,  verbose_name="Имя Пользователя")
    username = models.CharField(max_length=100,  verbose_name="Username Телеграм")

    def __str__(self):
        return f"№{self.id} ({self.user_id} - {self.name})"


