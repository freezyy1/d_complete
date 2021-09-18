from django.forms import ModelForm, BooleanField # Импортируем true-false поле
from .models import New


# Создаём модельную форму
class NewForm(ModelForm):
    check_box = BooleanField(label='подтвердите действие:')  # добавляем галочку, или же true-false поле

    # в класс мета как обычно надо написать модель по которой будет строится форма и нужные нам поля.
    # Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = New
        fields = ['post_name', 'position', 'category', 'author', 'content', 'check_box']
        # не забываем включить галочку в поля иначе она не будет показываться на странице!
