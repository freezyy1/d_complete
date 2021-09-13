from django.db import models
from django.core.validators import MinValueValidator

# новость: заголовок дата текст (весь) название
# новости: заголовок дата название текст (50 слов)
# Создаём модель товара
class New(models.Model):
    # имя
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    # описание
    description = models.TextField()
    # полный текст
    full_text = models.TextField()

    # дата
    data = models.DateField(auto_now_add = True)

    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='news',
    )

    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'


#  создаём категорию, к которой будет привязываться новость
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # названия категорий тоже не должны повторяться

    def __str__(self):
        return f'{self.name.title()}'
