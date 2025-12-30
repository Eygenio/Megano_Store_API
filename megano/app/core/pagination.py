from django.core.paginator import Paginator


def paginate_queryset(queryset, request, per_page=8):
    """
    Пагинация для страницы каталога товар и товар на скидке.

    :param per_page: Количество элементов на сттраницк
    """
    page = int(request.GET.get("currentPage", 1))
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)

    return {
        "items": page_obj.object_list,
        "currentPage": page,
        "lastPage": paginator.num_pages,
    }
