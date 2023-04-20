from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    # Criando um range de paginação
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_of_pages=4,
            current_page=1,

        )["pagination"]
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa: E501
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_of_pages=4,
            current_page=1  # Teste usuário na pág: 1
        )["pagination"]
        self.assertEqual([1, 2, 3, 4], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_of_pages=4,
            current_page=2  # Teste usuário na pág: 2
        )["pagination"]
        self.assertEqual([1, 2, 3, 4], pagination)

        # Here range should change
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_of_pages=4,
            current_page=3  # Teste usuário na pág: 3
        )["pagination"]
        self.assertEqual([2, 3, 4, 5], pagination)

        # Here range should change
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_of_pages=4,
            current_page=4  # Teste usuário na pág: 4
        )["pagination"]
        self.assertEqual([3, 4, 5, 6], pagination)

    def test_make_sure_middle_range_are_correct(self):
        # Here range should change
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_of_pages=4,
            current_page=10  # Teste usuário na pág: 10
        )["pagination"]
        self.assertEqual([9, 10, 11, 12], pagination)

        # Here range should change
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_of_pages=4,
            current_page=18  # Teste usuário na pág: 18
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)

    # testando se a paginação é estática como o ínicio
    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        # Here range should change
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_of_pages=4,
            current_page=19  # Teste usuário na pág: 19
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)

        # Here range should change
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_of_pages=4,
            current_page=20  # Teste usuário na pág: 20
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)

        # TESTE USUÁRIO ULTRAPASSANDO NÚMERO DE PÁG EXISTENTE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_of_pages=4,
            current_page=21  # Teste usuário na pág: 21
        )["pagination"]
        self.assertEqual([17, 18, 19, 20], pagination)
