from django import template

register = template.Library()  # обязательно нужно регать фильтр


@register.filter(name='multiply')
def multiply(value, arg):
    if isinstance(value, str) and isinstance(arg, int):
        return str(value) * arg
    else:
        raise ValueError(
            f'Нельзя умножить {type(value)} на {type(arg)}')


# если подгружать аргументы из шаблона, то фильтр будет работать
@register.filter(name='word_filter')
def censor(value, arg):
    words = value.split()
    value_output = ''
    for word in words:
        if isinstance(word, str) and isinstance(arg, str):
            if word == arg:
                # то, на что будет меняться мат
                word = '...'
            value_output += word + ' '
        else:
            raise ValueError(f'Нельзя {type(word)}!')
    return value_output
