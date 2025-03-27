try:
    from django import template
    from django.utils.safestring import mark_safe
except ImportError:
    raise ImportError(
        "Error: Django not installed. "
    )

register = template.Library()

def pluralize_ru(value, forms):
    """
    Склонение русских слов после числительных.
    Формат: "минута,минуты,минут"
    """
    try:
        number = abs(int(value))
        forms = [f.strip() for f in forms.split(",")]

        if len(forms) != 3:
            return ""

        # Обрабатываем особые случаи для чисел от 11 до 19
        if 11 <= number % 100 <= 19:
            return forms[2]

        # Получаем последнюю цифру для склонения
        last_digit = number % 10

        if last_digit == 1:
            return forms[0]
        elif 2 <= last_digit <= 4:
            return forms[1]
        elif last_digit == 0 or 5 <= last_digit <= 9:
            return forms[2]
        
        # Обрабатываем случаи для чисел типа 21, 31, 41, и так далее
        # Например, 21 комментарий, 31 комментарий
        if number % 10 == 1 and (number % 100 != 11):
            return forms[0]
        
        # Для чисел, оканчивающихся на 2, 3, 4, но не на 12, 13, 14 (например 22, 23, 24)
        if 2 <= number % 10 <= 4 and not (11 <= number % 100 <= 14):
            return forms[1]

        # Все остальные случаи для чисел >= 5
        return forms[2]

    except (ValueError, TypeError):
        return ""


register.filter("pluralize_ru", pluralize_ru)
