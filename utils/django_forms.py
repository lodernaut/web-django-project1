import re

from django.core.exceptions import ValidationError
from unidecode import unidecode


def strong_password(password):
    # utilizando expressão regular para validar password
    # positive lookahead
    regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$")

    if not regex.match(password):
        raise ValidationError(
            ("""Password must have at least one uppercase letter,
            one lowercase letter and one number. The length should be
            at least 8 character."""), code="invalid")


# def add_attr(field, attr_name, attr_new_val):
#     existing_attr = field.widget.attrs.get(attr_name, "")
#     field.widget.attrs[attr_name] = f"{existing_attr} {attr_new_val}".strip()


def add_placeholder(field, placeholder_val):
    field.widget.attrs["placeholder"] = placeholder_val


def add_class(field, class_val):
    field.widget.attrs["class"] = class_val


def add_label(field, label_val):
    field.label = label_val


def slugify(text):
    text = unidecode(text)  # remove acentos
    text = text.lower()  # transforma o texto em minúsculas
    text = re.sub(r'[^\w\s-]', '', text)  # remove caracteres não alfanuméricos
    # substitui espaços ou sublinhados por hífens
    text = re.sub(r'[\s_-]+', '-', text)
    # remove hífens no início ou no final da string
    text = re.sub(r'^-+|-+$', '', text)
    return text
