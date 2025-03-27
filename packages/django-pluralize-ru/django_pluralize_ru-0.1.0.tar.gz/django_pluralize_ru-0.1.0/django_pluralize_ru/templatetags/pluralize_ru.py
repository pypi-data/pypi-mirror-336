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

        if 11 <= number % 100 <= 19:
            return forms[2]

        last_digit = number % 10
        if last_digit == 1:
            return forms[0]
        elif 2 <= last_digit <= 4:
            return forms[1]
        return forms[2]

    except (ValueError, TypeError):
        return ""


register.filter("pluralize_ru", pluralize_ru)
