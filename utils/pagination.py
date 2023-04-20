from math import ceil


def make_pagination_range(
        page_range,
        total_pages,
        current_page):

    middle_range = ceil(total_pages / 2)
    start_range = current_page - middle_range  # range antes da atual
    stop_range = current_page + middle_range  # range atrás da atual

    # recebendo start_range só quando ele é negativo, se foi positivo recebe 0
    # recebe negativo convertido para positivo
    start_range_offset = abs(start_range) if start_range < 0 else 0

    # lógica para não retorna start_range negativo
    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    # python slice - fatiamento do page_range
    return page_range[start_range:stop_range]
