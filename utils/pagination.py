from math import ceil


def make_pagination_range(
        page_range,
        number_of_pages,
        current_page):

    middle_range = ceil(number_of_pages / 2)
    start_range = current_page - middle_range  # range antes da atual
    stop_range = current_page + middle_range  # range atrás da atual
    total_pages = len(page_range)

    # recebendo start_range só quando ele é negativo, se foi positivo recebe 0
    # recebe negativo convertido para positivo
    start_range_offset = abs(start_range) if start_range < 0 else 0

    # lógica para não retorna start_range negativo
    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    # lógica para quando current_page for  uma das 3 ultimas passar
    # a se estático e mostrar a 4 ultimas
    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    # python slice - fatiamento do page_range
    pagination = page_range[start_range:stop_range]
    return {
        "pagination": pagination,
        "page_range": page_range,
        "number_of_pages": number_of_pages,
        "current_page": current_page,
        "total_pages": total_pages,
        "start_range": start_range,
        "stop_range": stop_range,

        # saber se a primeira pág está sendo exibida
        "first_page_out_of_range": current_page > middle_range,

        # saber se a ultima pág está fora do range (não esta sendo exibida)
        "last_page_out_of_range": stop_range < total_pages,
    }
